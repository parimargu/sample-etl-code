from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from app.services.search_service import SearchService

router = APIRouter()

# Dependency
def get_search_service():
    return SearchService()

class SearchRequest(BaseModel):
    query: str
    limit: int = 10

class SearchResult(BaseModel):
    chunk_id: str
    doc_id: str
    text: str
    score: float

class DocumentResponse(BaseModel):
    doc_id: str
    text: str

@router.post("/search", response_model=List[SearchResult])
def search(request: SearchRequest, service: SearchService = Depends(get_search_service)):
    try:
        results = service.search(request.query, request.limit)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/document/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: str, service: SearchService = Depends(get_search_service)):
    doc = service.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
