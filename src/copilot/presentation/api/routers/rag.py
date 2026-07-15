"""RAG router — upload/index documents and search them.

POST /upload       ingest a PDF/MD/CSV/TXT into the vector store
POST /rag/search   semantic search over indexed chunks
GET  /rag/stats    number of indexed chunks
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, UploadFile

from copilot.application.use_cases.ingest_document import IngestDocumentUseCase
from copilot.application.use_cases.search_documents import SearchDocumentsUseCase
from copilot.domain.ports.vector_store import VectorStorePort
from copilot.presentation.api.dependencies import (
    get_ingest_document_use_case,
    get_search_documents_use_case,
    get_vector_store,
)
from copilot.presentation.api.schemas.rag import (
    RagStats,
    RetrievedChunkSchema,
    SearchRequest,
    SearchResponse,
    UploadResponse,
)

router = APIRouter(tags=["rag"])


@router.post("/upload", response_model=UploadResponse, summary="Upload & index a document")
async def upload(
    file: UploadFile = File(...),
    use_case: IngestDocumentUseCase = Depends(get_ingest_document_use_case),
) -> UploadResponse:
    data = await file.read()
    result = use_case.execute(file.filename or "upload", data, file.content_type)
    return UploadResponse(
        document_id=result.document_id,
        source=result.source,
        chunks_indexed=result.chunks_indexed,
    )


@router.post("/rag/search", response_model=SearchResponse, summary="Semantic search")
def search(
    request: SearchRequest,
    use_case: SearchDocumentsUseCase = Depends(get_search_documents_use_case),
) -> SearchResponse:
    chunks = use_case.execute(request.query, top_k=request.top_k)
    return SearchResponse(
        query=request.query,
        results=[RetrievedChunkSchema(text=c.text, source=c.source, score=c.score) for c in chunks],
    )


@router.get("/rag/stats", response_model=RagStats, summary="Index stats")
def stats(vector_store: VectorStorePort = Depends(get_vector_store)) -> RagStats:
    return RagStats(indexed_chunks=vector_store.count())
