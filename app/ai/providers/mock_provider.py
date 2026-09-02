"""
FOODARA AI - Mock Provider
Provider simulado para testing y fallback.
CLARAMENTE IDENTIFICADO COMO MOCK.
"""

from typing import List, Optional, Dict, Any
import asyncio
from app.ai.base import BaseAIProvider, AIMessage, AIResponse


class MockProvider(BaseAIProvider):
    """
    Provider simulado SOLO PARA DESARROLLO Y TESTING.
    
    ESTO NO ES UN PROVEEDOR REAL.
    Usad esto solo cuando no hay conexión a providers reales.
    """

    def __init__(self):
        super().__init__(api_key="mock-key")
        self.name = "MockProvider"

    async def chat(
        self,
        messages: List[AIMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AIResponse:
        """
        Respuesta simulada.
        Devuelve respuestas pre-hechas basadas en el contenido.
        """
        
        if not messages:
            return AIResponse(
                content="[MOCK] No hay mensajes",
                provider="mock",
                tokens_used=0,
                confidence=0.5,
            )

        last_message = messages[-1].content.lower()

        # Respuestas simuladas según el contenido
        if "compra" in last_message or "product" in last_message:
            response = "[MOCK RESPONSE] Te puedo ayudar a buscar productos alternativos con mejor relación precio-calidad."
        elif "receta" in last_message or "recipe" in last_message:
            response = "[MOCK RESPONSE] Aquí hay una receta sugerida basada en lo que tenés en la despensa."
        elif "presupuesto" in last_message or "budget" in last_message:
            response = "[MOCK RESPONSE] Con tu presupuesto podemos armar un plan de compras optimizado."
        elif "desperdicio" in last_message or "waste" in last_message:
            response = "[MOCK RESPONSE] Detecté productos próximos a vencer. Te sugiero usarlos pronto."
        else:
            response = f"[MOCK RESPONSE] Entendí: '{last_message[:50]}...'. Soy un provider simulado para testing."

        # Simular delay mínimo
        await asyncio.sleep(0.1)

        return AIResponse(
            content=response,
            provider="mock",
            tokens_used=len(response.split()),
            confidence=0.3,  # Baja confianza porque es mock
        )

    async def is_available(self) -> bool:
        """Mock está siempre disponible."""
        return True

    async def health_check(self) -> Dict[str, Any]:
        """Health check del mock."""
        return {
            "provider": "mock",
            "available": True,
            "status": "MOCK - ONLY FOR DEVELOPMENT",
            "warning": "Este es un provider simulado, no uses en producción",
        }
