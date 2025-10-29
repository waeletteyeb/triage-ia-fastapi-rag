# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Use the same environment variable names and defaults as original
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in environment (.env).")

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")  # optional
CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_db")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "guidelines")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL_REASON = "llama-3.3-70b-versatile"
TEMPERATURE_REASON = 0.2
TEMPERATURE_CHAT = 0.3
HTTP_TIMEOUT = 90

# Keep original default filename (note original had a typo "guidlines.json")
GUIDELINES_FILE = os.getenv("GUIDELINES_FILE", "guidelines.json")
