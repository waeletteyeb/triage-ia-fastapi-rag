# app/routes/chat.py
from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.groq import groq_chat
from app.config import TEMPERATURE_CHAT

router = APIRouter()


@router.post("/chat")
async def chat_with_triage_assistant(req: ChatRequest):
    user_text = (req.query or "").strip().lower()

    # Small-talk guardrails
    if user_text in {"hi", "hello", "hey"}:
        return {"reply": "Hello 👋 I’m your clinical triage assistant."}
    if user_text in {"ok", "okay", "thanks", "thank you"}:
        return {"reply": "You’re welcome ✅. Do you want more details about the triage?"}

    # Look for triage result in history (added by frontend)
    last_triage = None
    for m in reversed(req.history):
        if m.role == "system" and "triage_result" in m.content:
            last_triage = m.content
            break

    system_msg = (
        "You are a safe clinical assistant. You explain triage results, guidelines, "
        "and medical concepts. NEVER provide personal medical advice or dosing."
    )
    if last_triage:
        system_msg += f"\n\nContext: The last triage result was:\n{last_triage}"

    messages = [{"role": "system", "content": system_msg}]
    for m in req.history[-12:]:
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": req.query})

    reply = await groq_chat(messages, temperature=TEMPERATURE_CHAT, max_tokens=600)
    return {"reply": reply}
