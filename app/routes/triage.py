# app/routes/triage.py
from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from typing import List
from app.models.schemas import PatientInput
from app.services.analyzer import run_report_analyzer
from app.services.retrieval import collection
from app.services.reasoning import run_final_reasoning
from app.utils import extract_text_from_pdf_bytes, build_retrieval_query_from_analyzer

router = APIRouter()


@router.post("/triage")
async def triage_patient(input_data: PatientInput):
    """
    Full triage pipeline for raw text.
    """
    raw_text = ((input_data.text or "") + "\n" + (input_data.report or "")).strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="No input text or report provided.")

    # 1) Analyzer
    analyzer_json = await run_report_analyzer(raw_text)

    # 2) Retrieval
    retrieval_query = build_retrieval_query_from_analyzer(analyzer_json, raw_text)
    results = collection.query(query_texts=[retrieval_query], n_results=5)

    guideline_snippets: List[str] = []
    guideline_ids: List[str] = []
    if results and results.get("documents"):
        docs = results["documents"][0] or []
        ids_ = results.get("ids", [[]])[0] or []
        for d, gid in zip(docs, ids_):
            if d and str(d).strip():
                guideline_snippets.append(d)
                guideline_ids.append(gid)

    # 3) Final reasoning
    triage_json = await run_final_reasoning(analyzer_json, guideline_snippets)

    if input_data.debug:
        return {
            "triage": triage_json,
            "analyzer": analyzer_json,
            "retrieval_query": retrieval_query,
            "guideline_ids": guideline_ids,
            "guideline_snippets": guideline_snippets[:3],
        }
    return triage_json


@router.post("/triage-upload")
async def triage_upload(file: UploadFile = File(...), debug: bool = Query(default=False)):
    """
    Triage for uploaded .txt or .pdf.
    """
    fname = file.filename.lower()
    if fname.endswith(".txt"):
        raw_text = (await file.read()).decode("utf-8", errors="ignore")
    elif fname.endswith(".pdf"):
        pdf_bytes = await file.read()
        if not pdf_bytes:
            raise HTTPException(status_code=400, detail="Empty PDF file.")
        raw_text = extract_text_from_pdf_bytes(pdf_bytes)
        if not raw_text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from PDF.")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Use .txt or .pdf")

    # 1) Analyzer
    analyzer_json = await run_report_analyzer(raw_text)

    # 2) Retrieval
    retrieval_query = build_retrieval_query_from_analyzer(analyzer_json, raw_text)
    results = collection.query(query_texts=[retrieval_query], n_results=5)

    guideline_snippets: List[str] = []
    guideline_ids: List[str] = []
    if results and results.get("documents"):
        docs = results["documents"][0] or []
        ids_ = results.get("ids", [[]])[0] or []
        for d, gid in zip(docs, ids_):
            if d and str(d).strip():
                guideline_snippets.append(d)
                guideline_ids.append(gid)

    # 3) Final reasoning
    triage_json = await run_final_reasoning(analyzer_json, guideline_snippets)

    if debug:
        return {
            "triage": triage_json,
            "analyzer": analyzer_json,
            "retrieval_query": retrieval_query,
            "guideline_ids": guideline_ids,
            "guideline_snippets": guideline_snippets[:3],
        }
    return triage_json
