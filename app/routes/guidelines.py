# app/routes/guidelines.py
from fastapi import APIRouter, HTTPException
import os
import json
from app.services.retrieval import collection
from app.utils import _hash_id
from app.config import GUIDELINES_FILE

router = APIRouter()


@router.post("/ingest-guidelines")
def ingest_guidelines(payload: dict):
    """
    Payload:
    { "items": [
        {"id": "optional", "text": "guideline text", "metadata": {"source":"...", "level":"..."}}
      ]
    }
    """
    items = payload.get("items", [])
    if not items:
        raise HTTPException(status_code=400, detail="No items provided.")
    ids, docs, metas = [], [], []
    for it in items:
        text = (it.get("text") or "").strip()
        if not text:
            continue
        gid = (it.get("id") or _hash_id(text)).strip()
        ids.append(gid)
        docs.append(text)
        metas.append(it.get("metadata") or {})
    if not ids:
        raise HTTPException(status_code=400, detail="No valid guideline texts.")
    collection.add(ids=ids, documents=docs, metadatas=metas)
    return {"ingested": len(ids)}


def preload_guidelines():
    """
    Auto-load the GUIDELINES_FILE at startup (keeps the original filename default).
    """
    if not os.path.exists(GUIDELINES_FILE):
        print(f"⚠️ No {GUIDELINES_FILE} found, skipping preload")
        return
    try:
        with open(GUIDELINES_FILE, "r", encoding="utf-8") as f:
            items = json.load(f)
        if not isinstance(items, list):
            print(f"⚠️ {GUIDELINES_FILE} is not a list, skipping preload")
            return
        ids, docs, metas = [], [], []
        for it in items:
            text = (it.get("text") or "").strip()
            if not text:
                continue
            gid = (it.get("id") or _hash_id(text)).strip()
            ids.append(gid)
            docs.append(text)
            metas.append(it.get("metadata") or {})
        if ids:
            collection.add(ids=ids, documents=docs, metadatas=metas)
            print(f"✅ Preloaded {len(ids)} guidelines from {GUIDELINES_FILE}")
    except Exception as e:
        print(f"❌ Error loading {GUIDELINES_FILE}: {e}")
