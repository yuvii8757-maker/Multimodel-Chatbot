from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_session_id
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("/message", response_model=ChatMessageResponse)
async def send_chat_message(
    payload: ChatMessageRequest,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Process incoming chat message with optional web search, RAG retrieval,
    vision understanding, and emotional support guardrails.
    """
    try:
        response = await LLMService.process_chat(
            db=db,
            session_id=session_id,
            user_message=payload.message,
            conversation_id=payload.conversation_id,
            enable_web_search=payload.enable_web_search,
            enable_rag=payload.enable_rag,
            emotional_support_mode=payload.emotional_support_mode,
            attachment_ids=payload.attachment_ids
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat processing error: {str(e)}"
        )
