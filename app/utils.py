# app/utils.py
import hashlib
import io
import json
import re
from typing import List, Optional, Dict, Any

import pdfplumber
from fastapi import HTTPException

try:
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False


def _hash_id(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text using pdfplumber; per-page OCR fallback if no text and OCR_AVAILABLE.
    """
    try:
        texts: List[str] = []
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                t = t.strip()
                if t:
                    texts.append(t)
                elif OCR_AVAILABLE:
                    # Fast OCR path: rasterize page with pdfplumber (no external poppler call)
                    img = page.to_image(resolution=300).original
                    ocr_text = pytesseract.image_to_string(img) or ""
                    if ocr_text.strip():
                        texts.append(ocr_text.strip())
        return "\n\n".join([p for p in texts if p])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF extraction error: {str(e)}")


def build_retrieval_query_from_analyzer(an: Dict[str, Any], fallback_text: str) -> str:
    """
    Compact query from analyzer JSON to maximize embedding recall.
    """
    symptoms = an.get("symptoms") or []
    risks = an.get("risk_factors") or []
    diags = an.get("diagnoses") or an.get("diagnosis") or []
    parts = []
    if symptoms:
        parts.append("symptoms: " + ", ".join(symptoms))
    if risks:
        parts.append("risk_factors: " + ", ".join(risks))
    if diags:
        parts.append("diagnoses: " + ", ".join(diags))
    q = " | ".join(parts).strip()
    return q if q else (fallback_text or "")


def try_parse_json_strict(s: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(s)
    except Exception:
        return None


def extract_json_from_text(s: str) -> Optional[Dict[str, Any]]:
    """
    Last-resort extractor: finds largest {...} JSON-looking block.
    Keeps same behavior as original.
    """
    # Remove common code fences
    cleaned = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", s.strip(), flags=re.MULTILINE)
    # Try direct parse
    obj = try_parse_json_strict(cleaned)
    if obj is not None:
        return obj
    # Regex to find JSON object (kept same as original)
    match = re.search(r"\{(?:[^{}]|(?R))*\}", cleaned, flags=re.DOTALL)
    if match:
        return try_parse_json_strict(match.group(0))
    return None
