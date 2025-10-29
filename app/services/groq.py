# app/services/groq.py
import httpx
from typing import List, Dict, Any
from fastapi import HTTPException
from app.config import GROQ_CHAT_URL, GROQ_MODEL_REASON, HTTP_TIMEOUT, GROQ_API_KEY


async def groq_chat(
    messages: List[Dict[str, str]],
    temperature: float = 0.2,
    max_tokens: int = 800,
    force_json: bool = False,
) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": GROQ_MODEL_REASON,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if force_json:
        payload["response_format"] = {"type": "json_object"}

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        r = await client.post(GROQ_CHAT_URL, headers=headers, json=payload)
        if r.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Groq API error: {r.text}")
        # follow original shape
        return r.json()["choices"][0]["message"]["content"]
