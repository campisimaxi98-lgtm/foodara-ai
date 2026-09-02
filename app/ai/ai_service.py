"""
FOODARA AI - AI Service
Servicio central que orquesta todos los providers de IA.
"""

from typing import List, Optional, Dict, Any
import logging

from app.ai.base import BaseAIProvider, AIMessage, AIResponse
from app.ai.providers import ClaudeProvider, OpenAIProvider, MockProvider
from app.core.config import settings


logger = logging.getLogger(__name__)


class AIService:
    """
    Servicio de inteligencia artificial FOODARA.
    
    - Maneja múltiples providers
    - Fallback automático entre providers
    - Logging y monitoreo
    """

    def __init__(self):
        self.providers: Dict[str, BaseAIProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self) -> None:
        """Inicializar todos los providers disponibles."""
        
        # Claude (Anthropic)
        self.providers["claude"] = ClaudeProvider()

        # OpenAI
        self.providers["openai"] = OpenAIProvider()

        # Mock (siempre disponible como fallback)
        self.providers["mock"] = MockProvider()

        logger.info(f"Providers de IA inicializados: {list(self.providers.keys())}")

    async def _get_available_providers(self) -> List[str]:
        """Obtener lista de providers disponibles."""
        available = []
        for name, provider in self.providers.items():
            try:
                if await provider.is_available():
                    available.append(name)
            except Exception as e:
                logger.warning(f"Error verificando {name}: {str(e)}")
        return available

    async def chat(
        self,
        messages: List[AIMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        preferred_provider: Optional[str] = None,
    ) -> AIResponse:
        """
        Enviar mensajes a un provider de IA.
        
        Con fallback automático si el preferido no está disponible.
        
        Args:
            messages: Historial de conversación
            system_prompt: Instrucción del sistema
            temperature: Creatividad (0-1)
            max_tokens: Máximo de tokens
            preferred_provider: Provider preferido (claude, openai, mock)
        
        Returns:
            AIResponse con la respuesta
        """
        
        # Determinar provider preferido
        if preferred_provider is None:
            preferred_provider = settings.default_ai_provider

        # Lista de providers a intentar en orden
        providers_to_try = [preferred_provider]

        # Agregar providers como fallback
        available = await self._get_available_providers()
        for provider_name in available:
            if provider_name not in providers_to_try:
                providers_to_try.append(provider_name)

        # El provider mock es SOLO para desarrollo/testing y fallback explícito.
        # En producción NO debe servirse como respuesta automática al usuario.
        in_production = settings.app_env.lower() == "production"
        if in_production:
            providers_to_try = [p for p in providers_to_try if p != "mock"]
            if not providers_to_try:
                raise ValueError(
                    "Ningún provider de IA real está configurado. "
                    "Agregá ANTHROPIC_API_KEY o OPENAI_API_KEY y habilitá el provider en producción."
                )

        # Intentar con cada provider hasta que funcione
        last_error = None
        for provider_name in providers_to_try:
            try:
                if provider_name not in self.providers:
                    continue

                provider = self.providers[provider_name]

                if not await provider.is_available():
                    logger.warning(f"Provider {provider_name} no disponible")
                    continue

                logger.info(f"Usando provider: {provider_name}")

                response = await provider.chat(
                    messages=messages,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                return response

            except Exception as e:
                logger.warning(f"Error con {provider_name}: {str(e)}")
                last_error = e
                continue

        # Si llegamos aquí, todos fallaron
        error_msg = f"Ningún provider de IA disponible. Último error: {str(last_error)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    async def health_check(self) -> Dict[str, Any]:
        """Verificar salud de todos los providers."""
        health = {}
        for name, provider in self.providers.items():
            try:
                health[name] = await provider.health_check()
            except Exception as e:
                health[name] = {
                    "provider": name,
                    "available": False,
                    "error": str(e),
                }
        return health

    async def get_providers_status(self) -> Dict[str, bool]:
        """Obtener estado de disponibilidad de todos los providers."""
        status = {}
        for name, provider in self.providers.items():
            try:
                status[name] = await provider.is_available()
            except Exception:
                status[name] = False
        return status

    async def aclose(self) -> None:
        """Cerrar clientes HTTP de los providers."""
        for provider in self.providers.values():
            ac = getattr(provider, "aclose", None)
            if ac is not None:
                try:
                    await ac()
                except Exception:
                    logger.warning("Error cerrando HTTP client del provider", exc_info=True)


# Instancia global
_ai_service: Optional[AIService] = None


async def get_ai_service() -> AIService:
    """Obtener instancia (singleton) del servicio de IA."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service


async def close_ai_service() -> None:
    """Cerrar los recursos del servicio de IA (en shutdown)."""
    global _ai_service
    if _ai_service is not None:
        await _ai_service.aclose()
        _ai_service = None


# Instancia global
_ai_service: Optional[AIService] = None


async def get_ai_service() -> AIService:
    """Obtener instancia del servicio de IA."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
