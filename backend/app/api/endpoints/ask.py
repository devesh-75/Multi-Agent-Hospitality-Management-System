"""
Natural Language Q&A Endpoint
Answers operational and financial questions using hybrid SQL + RAG retrieval.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.app.core.database import get_db
from backend.app.schemas.dto import AskRequest, AskResponse
from rag.retrieval import RAGService

router = APIRouter(tags=["Question Answering"])

@router.post("/ask", response_model=AskResponse)
def ask_question(
    req: AskRequest,
    db: Session = Depends(get_db)
):
    rag_service = RAGService(db)
    result = rag_service.query(question=req.question, property_id=req.property_id)
    return AskResponse(
        question=req.question,
        answer=result["answer"],
        sources=result["sources"],
        structured_data=result.get("structured_data"),
        confidence=result.get("confidence", "HIGH"),
        data_limitations=result.get("data_limitations")
    )
