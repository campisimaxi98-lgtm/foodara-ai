"""
FOODARA AI - Base AI Provider
Interfaz abstracta para todos los providers de IA.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class AIMessage(BaseModel):
    """Formato estándar de mensaje en FOODARA."""
    role: str  # "user" o "assistant"
    content: str


class AIResponse(BaseModel):
    """Respuesta estándar de un provider de IA."""
    content: str
    provider: str
    tokens_used: int = 0
    confidence: float = 1.0


class BaseAIProvider(ABC):
    """
    Interfaz base para todos los providers de IA.
    
    Permite cambiar entre OpenAI, Claude, Local, etc.
    sin cambiar el código que los usa.
    """

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.name: str = self.__class__.__name__

    @abstractmethod
    async def chat(
        self,
        messages: List[AIMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> AIResponse:
        """
        Enviar mensajes al modelo de IA.
        
        Args:
            messages: Historial de conversación
            system_prompt: Instrucción del sistema
            temperature: Creatividad (0-1)
            max_tokens: Máximo de tokens en respuesta
        
        Returns:
            AIResponse con la respuesta
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Verificar si el provider está disponible."""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Verificar salud del provider."""
        pass
