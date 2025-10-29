# app/models/schemas.py
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class PatientInput(BaseModel):
    text: Optional[str] = None
    report: Optional[str] = None
    debug: Optional[bool] = False


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    history: List[ChatMessage] = Field(default_factory=list)
    query: str


class HandoffRequest(BaseModel):
    patient: Dict[str, Any]
    triage: Dict[str, Any]
    instruction: str
