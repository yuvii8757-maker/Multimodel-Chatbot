from app.core.config import settings
from app.services.providers.base import (
    BaseLLMProvider,
    BaseVisionProvider,
    BaseEmbeddingProvider,
    BaseAudioProvider
)
from app.services.providers.mock_provider import (
    MockLLMProvider,
    MockVisionProvider,
    MockEmbeddingProvider,
    MockAudioProvider
)
from app.services.providers.openai_provider import (
    OpenAILLMProvider,
    OpenAIVisionProvider,
    OpenAIEmbeddingProvider,
    OpenAIAudioProvider
)


def get_llm_provider() -> BaseLLMProvider:
    # If LLM_PROVIDER is mock or OPENAI_API_KEY is not set, use MockLLMProvider
    if settings.LLM_PROVIDER == "mock" or not settings.OPENAI_API_KEY:
        return MockLLMProvider()
    return OpenAILLMProvider()


def get_vision_provider() -> BaseVisionProvider:
    if settings.LLM_PROVIDER == "mock" or not settings.OPENAI_API_KEY:
        return MockVisionProvider()
    return OpenAIVisionProvider()


def get_embedding_provider() -> BaseEmbeddingProvider:
    if settings.LLM_PROVIDER == "mock" or not settings.OPENAI_API_KEY:
        return MockEmbeddingProvider(dimension=settings.EMBEDDING_DIMENSION)
    return OpenAIEmbeddingProvider()


def get_audio_provider() -> BaseAudioProvider:
    if settings.LLM_PROVIDER == "mock" or not settings.OPENAI_API_KEY:
        return MockAudioProvider()
    return OpenAIAudioProvider()
