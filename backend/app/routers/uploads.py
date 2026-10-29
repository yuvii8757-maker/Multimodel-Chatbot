import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_session_id, sanitize_filename
from app.core.config import settings
from app.db.models import Attachment

router = APIRouter(prefix="/api/uploads", tags=["Uploads"])


@router.post("")
async def upload_attachment(
    file: UploadFile = File(...),
    session_id: str = Depends(get_session_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload an attachment (image, audio, document) for chat messaging.
    Saves file to local disk and returns metadata and attachment ID.
    """
    filename = sanitize_filename(file.filename or "attachment")
    content = await file.read()

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Attachment exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    ext = os.path.splitext(filename)[1].lower()
    mime = file.content_type or "application/octet-stream"

    # Determine broad file type
    if ext in [".png", ".jpg", ".jpeg", ".webp", ".gif"] or "image" in mime:
        file_type = "image"
    elif ext in [".mp3", ".wav", ".webm", ".m4a", ".ogg"] or "audio" in mime:
        file_type = "audio"
    else:
        file_type = "document"

    session_upload_dir = os.path.join(settings.UPLOAD_DIR, session_id)
    os.makedirs(session_upload_dir, exist_ok=True)
    file_id = uuid.uuid4().hex[:10]
    saved_path = os.path.join(session_upload_dir, f"{file_id}_{filename}")

    with open(saved_path, "wb") as f:
        f.write(content)

    att = Attachment(
        id=str(uuid.uuid4()),
        message_id=None,  # will be linked when message is sent
        file_name=filename,
        file_type=file_type,
        mime_type=mime,
        file_path=saved_path,
        file_size=len(content)
    )
    db.add(att)
    await db.commit()
    await db.refresh(att)

    return {
        "id": att.id,
        "file_name": att.file_name,
        "file_type": att.file_type,
        "mime_type": att.mime_type,
        "file_size": att.file_size,
        "created_at": att.created_at
    }
