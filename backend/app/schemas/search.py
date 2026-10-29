from typing import List, Optional
from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    title: str
    url: str
    snippet: str
    score: Optional[float] = None


class SearchQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=500)
    max_results: int = Field(default=5, ge=1, le=10)


class SearchQueryResponse(BaseModel):
    query: str
    provider: str
    results: List[SearchResultItem] = Field(default_factory=list)
