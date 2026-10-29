from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.core.security import get_session_id
from app.db.models import Conversation, Message, Attachment
from app.schemas.chat import ConversationSummary, ConversationDetail, MessageItem, AttachmentInfo

router = APIRouter(prefix="/api/conversations", tags=["Conversations"])


@router.get("", response_model=List[ConversationSummary])
async def list_conversations(
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    """List all conversations belonging to the anonymous session."""
    stmt = (
        select(Conversation)
        .where(Conversation.session_id == session_id)
        .order_by(Conversation.updated_at.desc())
    )
    res = await db.execute(stmt)
    conversations = res.scalars().all()

    summaries = []
    for conv in conversations:
        # Count messages
        cnt_stmt = select(func.count(Message.id)).where(Message.conversation_id == conv.id)
        cnt_res = await db.execute(cnt_stmt)
        count = cnt_res.scalar_one_or_none() or 0

        summaries.append(ConversationSummary(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=count
        ))
    return summaries


@router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: str,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    """Fetch complete conversation history with messages and attachments."""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.session_id == session_id
    )
    res = await db.execute(stmt)
    conv = res.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

    msg_stmt = (
        select(Message)
        .where(Message.conversation_id == conv.id)
        .order_by(Message.created_at.asc())
    )
    msg_res = await db.execute(msg_stmt)
    messages = msg_res.scalars().all()

    formatted_messages = []
    for m in messages:
        # Load attachments
        att_stmt = select(Attachment).where(Attachment.message_id == m.id)
        att_res = await db.execute(att_stmt)
        atts = att_res.scalars().all()

        formatted_messages.append(MessageItem(
            id=m.id,
            conversation_id=m.conversation_id,
            role=m.role,
            content=m.content,
            msg_metadata=m.msg_metadata or {},
            attachments=[
                AttachmentInfo(
                    id=a.id,
                    file_name=a.file_name,
                    file_type=a.file_type,
                    mime_type=a.mime_type,
                    file_size=a.file_size,
                    created_at=a.created_at
                ) for a in atts
            ],
            created_at=m.created_at
        ))

    return ConversationDetail(
        id=conv.id,
        title=conv.title,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        messages=formatted_messages
    )


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    """Delete a conversation and its messages."""
    stmt = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.session_id == session_id
    )
    res = await db.execute(stmt)
    conv = res.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found.")

    await db.delete(conv)
    await db.commit()
    return {"status": "success", "message": "Conversation deleted."}
