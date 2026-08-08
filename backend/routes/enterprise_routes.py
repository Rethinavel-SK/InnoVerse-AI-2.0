import uuid
import logging
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from rag.rag_service import rag_service
from agents.collaboration.collaboration_bus import collaboration_bus
from services.doc_generator import doc_generator

router = APIRouter(prefix="/api/v1", tags=["Enterprise Capabilities"])
logger = logging.getLogger(__name__)

class SearchQuery(BaseModel):
    query: str
    top_k: int = 4

class CollaborationRequest(BaseModel):
    problem_statement: str
    session_id: Optional[str] = None

class DocumentGenRequest(BaseModel):
    problem_statement: str
    report: Dict[str, Any]

# --- RAG KNOWLEDGE BASE ENDPOINTS ---

@router.post("/rag/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        doc = rag_service.upload_and_index(content, file.filename)
        return {
            "status": "success",
            "message": f"Document '{file.filename}' indexed into RAG vector store successfully.",
            "document": doc.dict()
        }
    except Exception as e:
        logger.error(f"RAG upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rag/documents")
async def list_documents():
    docs = rag_service.list_documents()
    return {"documents": [d.dict() for d in docs]}

@router.post("/rag/search")
async def search_knowledge_base(body: SearchQuery):
    results = rag_service.search_similar_chunks(body.query, top_k=body.top_k)
    return {"query": body.query, "results": [r.dict() for r in results]}

@router.delete("/rag/documents/{doc_id}")
async def delete_document(doc_id: str):
    success = rag_service.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"status": "success", "message": f"Document '{doc_id}' removed from RAG index."}

# --- AGENT COLLABORATION ENDPOINTS ---

@router.post("/collaboration/execute")
async def execute_collaboration(body: CollaborationRequest):
    sess_id = body.session_id or str(uuid.uuid4())[:8]
    logs = await collaboration_bus.execute_collaboration_pass(sess_id, body.problem_statement)
    return {
        "session_id": sess_id,
        "status": "completed",
        "total_messages": len(logs),
        "collaboration_logs": logs
    }

@router.get("/collaboration/logs/{session_id}")
async def get_collaboration_logs(session_id: str):
    logs = collaboration_bus.get_collaboration_logs(session_id)
    return {"session_id": session_id, "logs": [m.dict() for m in logs]}

# --- AI PITCH DECK & SRS GENERATOR ENDPOINTS ---

@router.post("/documents/pitch-deck")
async def generate_pitch_deck(body: DocumentGenRequest):
    slides = doc_generator.generate_pitch_deck(body.report, body.problem_statement)
    return {"status": "success", "total_slides": len(slides), "slides": slides}

@router.post("/documents/srs")
async def generate_srs(body: DocumentGenRequest):
    sections = doc_generator.generate_srs_document(body.report, body.problem_statement)
    return {"status": "success", "total_sections": len(sections), "sections": sections}
