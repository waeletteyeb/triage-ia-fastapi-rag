# app/services/reasoning.py
import json
from typing import Dict, Any, List
from app.services.groq import groq_chat
from app.utils import extract_json_from_text
from app.config import TEMPERATURE_REASON


async def run_final_reasoning(analyzer_json: Dict[str, Any], guideline_snippets: List[str]) -> Dict[str, Any]:
    """
    Produce STRICT JSON:
      triage_level: string
      explanation: string
      recommendations: string[]
    """
    facts = json.dumps(analyzer_json, ensure_ascii=False)
    ctx = "\n\n".join(guideline_snippets) if guideline_snippets else "No relevant guidelines found."

    sys_prompt = (
        "You are a clinical triage assistant. "
        "Return STRICT JSON (no markdown, no code fences). "
        "Keys:\n"
        " - triage_level (string; e.g., 'Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5', or 'Unknown')\n"
        " - explanation (string; concise, grounded in facts/guidelines)\n"
        " - recommendations (array of short actionable strings)\n"
        "If no guidelines are available, infer a cautious triage level from facts; if insufficient, use 'Unknown'."
    )
    user_prompt = f"Structured patient facts:\n{facts}\n\nRetrieved guideline snippets:\n{ctx}\n\nReturn ONLY the JSON."

    content = await groq_chat(
        messages=[{"role": "system", "content": sys_prompt},
                  {"role": "user", "content": user_prompt}],
        temperature=TEMPERATURE_REASON,
        max_tokens=700,
        force_json=True,  # <- Enforce pure JSON
    )

    parsed = extract_json_from_text(content)
    if parsed is None:
        # Last resort fallback: safe default
        return {
            "triage_level": "Unknown",
            "explanation": "Unable to parse model output into JSON.",
            "recommendations": ["Consult a healthcare professional for further evaluation and guidance."],
        }
    # Ensure schema is present (same as original)
    triage_level = str(parsed.get("triage_level", "Unknown")).strip() or "Unknown"
    explanation = str(parsed.get("explanation", "")).strip() or "No explanation provided."
    recommendations = parsed.get("recommendations", [])
    if isinstance(recommendations, str):
        recommendations = [recommendations]
    elif not isinstance(recommendations, list):
        recommendations = []
    recommendations = [str(x).strip() for x in recommendations if str(x).strip()]
    return {
        "triage_level": triage_level,
        "explanation": explanation,
        "recommendations": recommendations,
    }
