# app/routes/n8n_handoff.py
from fastapi import APIRouter, HTTPException
import httpx
from app.models.schemas import HandoffRequest
from app.config import N8N_WEBHOOK_URL, HTTP_TIMEOUT

router = APIRouter()


@router.post("/handoff-n8n")
async def handoff_to_n8n(req: HandoffRequest):
    """
    Optional: hand off the triage JSON + patient info to an n8n webhook.
    """
    if not N8N_WEBHOOK_URL:
        raise HTTPException(status_code=500, detail="Missing N8N_WEBHOOK_URL in .env")

    payload = {
        "patient": req.patient,
        "triage": req.triage,
        "instruction": req.instruction,
    }
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        try:
            r = await client.post(N8N_WEBHOOK_URL, json=payload)
            if r.status_code != 200:
                # Surface n8n error message clearly
                raise HTTPException(status_code=500, detail=f"n8n error: {r.text}")
            # Return n8n JSON (if any)
            try:
                return r.json()
            except Exception:
                return {"status": "ok", "message": "Handoff sent to n8n."}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error calling n8n: {str(e)}")
