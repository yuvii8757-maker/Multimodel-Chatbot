from fastapi import APIRouter, HTTPException, status
from app.schemas.search import SearchQueryRequest, SearchQueryResponse, SearchResultItem
from app.services.web_search_service import WebSearchService

router = APIRouter(prefix="/api/search", tags=["Web Search"])


@router.post("", response_model=SearchQueryResponse)
async def perform_search(payload: SearchQueryRequest):
    """Execute standalone web search using Tavily or DuckDuckGo fallback."""
    try:
        search_data = await WebSearchService.search(payload.query, max_results=payload.max_results)
        items = [
            SearchResultItem(
                title=r["title"],
                url=r["url"],
                snippet=r["snippet"],
                score=r.get("score")
            ) for r in search_data.get("results", [])
        ]
        return SearchQueryResponse(
            query=payload.query,
            provider=search_data.get("provider", "unknown"),
            results=items
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search service error: {str(e)}"
        )
