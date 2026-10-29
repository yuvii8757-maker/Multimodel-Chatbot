from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import Response
from app.schemas.audio import TranscribeResponse, SynthesizeRequest
from app.services.audio_service import AudioService

router = APIRouter(prefix="/api/audio", tags=["Audio"])


@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(file: UploadFile = File(...)):
    """Transcribe an uploaded voice note or audio file to text."""
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty audio file.")
        
        transcript = await AudioService.transcribe(content, filename=file.filename or "audio.webm")
        return TranscribeResponse(text=transcript)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech transcription failed: {str(e)}"
        )


@router.post("/synthesize")
async def synthesize_speech(payload: SynthesizeRequest):
    """Synthesize text into speech MP3 audio stream."""
    try:
        audio_bytes = await AudioService.synthesize(text=payload.text, voice=payload.voice or "alloy")
        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={"Content-Disposition": 'inline; filename="speech.mp3"'}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech synthesis failed: {str(e)}"
        )
