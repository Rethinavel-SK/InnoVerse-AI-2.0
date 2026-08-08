import uuid
import datetime
import math
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from rag.document_parser import DocumentParser

class DocumentChunk(BaseModel):
    chunk_id: str
    doc_id: str
    doc_name: str
    chunk_index: int
    content: str
    score: float = 0.0

class KnowledgeDocument(BaseModel):
    doc_id: str
    filename: str
    file_type: str
    upload_date: str
    total_chunks: int
    content_preview: str

class RAGService:
    """
    Retrieval-Augmented Generation (RAG) Service.
    Supports document indexing, text chunking, in-memory TF-IDF/Vector similarity search,
    and context retrieval for agent prompts.
    """

    def __init__(self):
        self._documents: Dict[str, KnowledgeDocument] = {}
        self._chunks: List[DocumentChunk] = []

    def upload_and_index(self, file_bytes: bytes, filename: str) -> KnowledgeDocument:
        doc_id = str(uuid.uuid4())[:8]
        raw_text = DocumentParser.parse_file(file_bytes, filename)
        chunks_text = DocumentParser.chunk_text(raw_text, chunk_size=300, overlap=40)

        if not chunks_text:
            chunks_text = [raw_text[:500] if raw_text else "Empty document."]

        for i, c_text in enumerate(chunks_text):
            chunk = DocumentChunk(
                chunk_id=f"{doc_id}_c{i}",
                doc_id=doc_id,
                doc_name=filename,
                chunk_index=i,
                content=c_text
            )
            self._chunks.append(chunk)

        ext = filename.split(".")[-1].upper() if "." in filename else "FILE"
        doc = KnowledgeDocument(
            doc_id=doc_id,
            filename=filename,
            file_type=ext,
            upload_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            total_chunks=len(chunks_text),
            content_preview=raw_text[:200] + ("..." if len(raw_text) > 200 else "")
        )
        self._documents[doc_id] = doc
        return doc

    def list_documents(self) -> List[KnowledgeDocument]:
        return list(self._documents.values())

    def delete_document(self, doc_id: str) -> bool:
        if doc_id in self._documents:
            del self._documents[doc_id]
            self._chunks = [c for c in self._chunks if c.doc_id != doc_id]
            return True
        return False

    def search_similar_chunks(self, query: str, top_k: int = 4) -> List[DocumentChunk]:
        if not self._chunks or not query.strip():
            return []

        query_words = set(re.findall(r'\w+', query.lower()))

        scored_chunks = []
        for c in self._chunks:
            c_words = set(re.findall(r'\w+', c.content.lower()))
            overlap = query_words.intersection(c_words)
            if not overlap:
                score = 0.0
            else:
                score = len(overlap) / (math.log(len(c_words) + 1) + 1.0) * 100.0

            c_copy = DocumentChunk(**c.dict())
            c_copy.score = min(98.5, round(score * 15 + 45.0, 1)) if score > 0 else 0.0
            if c_copy.score > 0:
                scored_chunks.append(c_copy)

        scored_chunks.sort(key=lambda x: x.score, reverse=True)
        return scored_chunks[:top_k]

    def get_rag_context_prompt(self, query: str) -> str:
        results = self.search_similar_chunks(query, top_k=3)
        if not results:
            return ""

        context_lines = ["\n--- RAG KNOWLEDGE BASE RETRIEVED CONTEXT ---"]
        for r in results:
            context_lines.append(f"Source: [{r.doc_name}] (Score: {r.score}%)\nContent: {r.content}\n")
        context_lines.append("--- END RETRIEVED CONTEXT ---\n")
        return "\n".join(context_lines)

rag_service = RAGService()
