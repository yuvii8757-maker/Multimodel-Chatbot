from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class KnowledgeDocumentResponse(BaseModel):
    id: str
    title: str
    file_name: str
    file_size: int
    total_chunks: int
    created_at: datetime


class DocumentChunkResponse(BaseModel):
    id: str
    chunk_index: int
    chunk_text: str
    chunk_metadata: Optional[Dict[str, Any]] = None


class DocumentCreateRequest(BaseModel):
    prompt: str = Field(..., min_length=2, max_length=5000)
    title: Optional[str] = "Generated Document"
    context: Optional[str] = None


class DocumentEditRequest(BaseModel):
    document_id: Optional[str] = None
    original_content: str = Field(..., min_length=1)
    instruction: str = Field(..., min_length=1, max_length=2000)  # e.g. "summarize", "rewrite", "fix grammar", "translate to Spanish", or custom
    action_type: Optional[str] = "custom"  # "summarize", "grammar", "rewrite", "translate", "custom"
    target_language: Optional[str] = "English"


class DiffChunk(BaseModel):
    type: str  # "equal", "insert", "delete"
    text: str


class DocumentEditResponse(BaseModel):
    document_id: Optional[str] = None
    title: str
    original_content: str
    revised_content: str
    diff_chunks: List[DiffChunk] = Field(default_factory=list)
    version_number: int = 1
    status: str = "revised"


class DocumentVersionResponse(BaseModel):
    id: str
    title: str
    status: str
    version_number: int
    created_at: datetime
    updated_at: datetime
