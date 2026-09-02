"""
FOODARA AI - Anthropic Claude Provider
Integration con Anthropic Claude API.
"""

from typing import List, Optional, Dict, Any
import httpx
from app.ai.base import BaseAIProvider, AIMessage, AIResponse
from app.core.config import settings


class ClaudeProvider(BaseAIProvider):
    """
    Provider para Anthropic Claude.
    
    API Docs: https://docs.anthropic.com/
    """

    def __init__(self):
        super().__init__(api_key=settings.anthropic_api_key)
        self.model = settings.anthropic_model
        self.api_url = "https://api.anthropic.com/v1/messages"
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
        """Enviar mensajes a Claude."""
        
        if not await self.is_available():
            raise ValueError("Claude provider no disponible")

        # Construir headers
        headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": self.api_key,
        }

        # Construir request
        system = system_prompt or "Eres FOODARA AI, un asistente inteligente de alimentación para usuarios en Argentina. Ayudas a comprar mejor, comer mejor y desperdiciar menos."

        body = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system,
            "messages": [
                {"role": msg.role, "content": msg.content}
                for msg in messages
            ],
            "temperature": temperature,
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

            blocks = data.get("content") or []
            if not blocks:
                raise ValueError("Claude devolvió una respuesta vacía")
            content = blocks[0].get("text", "")
            tokens_used = (
                data.get("usage", {}).get("input_tokens", 0) +
                data.get("usage", {}).get("output_tokens", 0)
            )

            return AIResponse(
                content=content,
                provider="claude",
                tokens_used=tokens_used,
                confidence=0.95,
            )
        except httpx.RequestError as e:
            raise ValueError(f"Error conectando con Claude API: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error en Claude provider: {str(e)}")

    async def is_available(self) -> bool:
        """Verificar si Claude está disponible."""
        if not settings.anthropic_enabled:
            return False
        if not self.api_key:
            return False
        return True

    async def health_check(self) -> Dict[str, Any]:
        """Verificar salud del provider."""
        return {
            "provider": "claude",
            "available": await self.is_available(),
            "model": self.model,
            "api_configured": bool(self.api_key),
        }
