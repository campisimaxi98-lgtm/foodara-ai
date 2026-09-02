"""
FOODARA AI - OpenAI Provider
Integration con OpenAI API.
"""

from typing import List, Optional, Dict, Any
import httpx
from app.ai.base import BaseAIProvider, AIMessage, AIResponse
from app.core.config import settings


class OpenAIProvider(BaseAIProvider):
    """
    Provider para OpenAI GPT.
    
    API Docs: https://platform.openai.com/docs/
    """

    def __init__(self):
        super().__init__(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Reutilizar un único cliente HTTP para evitar overhead de conexión."""
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=30.0)
        return self._client

    async def aclose(self) -> None:
        """Cerrar el cliente HTTP del provider."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def chat(
        self,
        messages: List[AIMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AIResponse:
        """Enviar mensajes a OpenAI."""
        
        if not await self.is_available():
            raise ValueError("OpenAI provider no disponible")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        system = system_prompt or "Eres FOODARA AI, un asistente inteligente de alimentación para usuarios en Argentina."

        messages_list = [
            {"role": "system", "content": system},
            *[
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ]
        ]

        body = {
            "model": self.model,
            "messages": messages_list,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        try:
            client = await self._get_client()
            response = await client.post(
                self.api_url,
                json=body,
                headers=headers
            )
            response.raise_for_status()
            data = response.json()

            choices = data.get("choices") or []
            if not choices:
                raise ValueError("OpenAI devolvió una respuesta vacía")
            content = choices[0].get("message", {}).get("content", "")
            tokens_used = data.get("usage", {}).get("total_tokens", 0)

            return AIResponse(
                content=content,
                provider="openai",
                tokens_used=tokens_used,
                confidence=0.95,
            )
        except httpx.RequestError as e:
            raise ValueError(f"Error conectando con OpenAI API: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error en OpenAI provider: {str(e)}")

    async def is_available(self) -> bool:
        """Verificar si OpenAI está disponible."""
        if not settings.openai_enabled:
            return False
        if not self.api_key:
            return False
        return True

    async def health_check(self) -> Dict[str, Any]:
        """Verificar salud del provider."""
        return {
            "provider": "openai",
            "available": await self.is_available(),
            "model": self.model,
            "api_configured": bool(self.api_key),
        }
