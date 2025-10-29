# app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routes import triage, chat, guidelines, n8n_handoff
from app.routes.guidelines import preload_guidelines

app = FastAPI(title="AI Triage System (Analyzer + BioGPT + Chroma + Llama/Groq)")

# CORS for local Streamlit or web UIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(triage.router)
app.include_router(chat.router)
app.include_router(guidelines.router)
app.include_router(n8n_handoff.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "AI Triage API (Analyzer + BioGPT + Chroma + Llama/Groq)"}


# Preload guidelines at startup
preload_guidelines()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(__import__("os").environ.get("PORT", "8000")), reload=True)
