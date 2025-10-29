# app/services/analyzer.py
from typing import Dict, Any
from app.services.groq import groq_chat
from app.utils import extract_json_from_text


async def run_report_analyzer(raw_text: str) -> Dict[str, Any]:
    """
    Extract compact JSON with keys:
      - symptoms: list[str]
      - risk_factors: list[str]
      - diagnoses: list[str]
    Always returns a dict with those keys (lists).
    """
    sys_prompt = (
        "You are a medical report analyzer. "
        "Return ONLY a valid JSON object (no markdown, no code fences) with keys:\n"
        "symptoms (array of short phrases), risk_factors (array), diagnoses (array)."
    )
    user_prompt = f"Report / Notes:\n{raw_text}"

    content = await groq_chat(
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": user_prompt}],
        temperature=0.1,
        max_tokens=400,
        force_json=True,  # <- Enforce pure JSON
    )

    data = extract_json_from_text(content) or {"symptoms": [], "risk_factors": [], "diagnoses": []}
    # Normalize to lists (same as original)
    for k in ["symptoms", "risk_factors", "diagnoses"]:
        v = data.get(k, [])
        if isinstance(v, str):
            data[k] = [v]
        elif isinstance(v, list):
            data[k] = [str(x) for x in v if str(x).strip()]
        else:
            data[k] = []
    return data
