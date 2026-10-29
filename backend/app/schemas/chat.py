from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AttachmentInfo(BaseModel):
    id: str
    file_name: str
    file_type: str
    mime_type: str
    file_size: int
    created_at: datetime


class MessageItem(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    msg_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    attachments: List[AttachmentInfo] = Field(default_factory=list)
    created_at: datetime


class ChatMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(..., min_length=1, max_length=10000)
    enable_web_search: bool = False
    enable_rag: bool = True
    emotional_support_mode: bool = False
    # Optional direct attachment id or file path attached to this message
    attachment_ids: Optional[List[str]] = Field(default_factory=list)


class ChatMessageResponse(BaseModel):
    conversation_id: str
    message_id: str
    role: str = "assistant"
    content: str
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    web_sources: List[Dict[str, Any]] = Field(default_factory=list)
    audio_url: Optional[str] = None
    created_at: datetime


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0


class ConversationDetail(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageItem] = Field(default_factory=list)
