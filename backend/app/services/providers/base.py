from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseLLMProvider(ABC):
    """Abstract interface for LLM text generation."""

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate response text given message history."""
        pass


class BaseVisionProvider(ABC):
    """Abstract interface for vision / image understanding."""

    @abstractmethod
    async def analyze_image(
        self,
        image_bytes: bytes,
        prompt: str,
        mime_type: str = "image/jpeg"
    ) -> str:
        """Analyze an image and return visual description / answers."""
        pass


class BaseEmbeddingProvider(ABC):
    """Abstract interface for vector embeddings."""

    @abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate dense embedding vectors for input texts."""
        pass


class BaseAudioProvider(ABC):
    """Abstract interface for Speech-to-Text and Text-to-Speech."""

    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, filename: str) -> str:
        """Transcribe audio bytes to text."""
        pass

    @abstractmethod
    async def synthesize(self, text: str, voice: str = "alloy") -> bytes:
        """Synthesize text into speech audio bytes (MP3)."""
        pass
