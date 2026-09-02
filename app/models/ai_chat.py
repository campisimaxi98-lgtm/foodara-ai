"""
FOODARA AI - AI Chat Models
Modelos para conversaciones y mensajes con IA.
"""

from sqlalchemy import String, Integer, Column, ForeignKey, Text, Boolean, Float
from sqlalchemy.orm import relationship

from app.database.base import Base, IDMixin, TimeStampMixin


class AIConversation(Base, IDMixin, TimeStampMixin):
    """
    Conversación del usuario con FOODARA AI.
    Historial de interacciones.
    """
    __tablename__ = "ai_conversations"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic = Column(String(255), nullable=True)  # shopping, menu, waste, general, etc.

    is_active = Column(Boolean, default=True)

    # Relaciones
    user = relationship("User", back_populates="conversations")
    messages = relationship(
        "AIMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AIConversation(id={self.id}, user_id={self.user_id}, topic={self.topic})>"


class AIMessage(Base, IDMixin, TimeStampMixin):
    """
    Mensaje individual en una conversación.
    Puede ser del usuario o de FOODARA AI.
    """
    __tablename__ = "ai_messages"

    conversation_id = Column(Integer, ForeignKey("ai_conversations.id"), nullable=False)

    # Información del mensaje
    role = Column(String(20), nullable=False)  # "user" o "assistant"
    content = Column(Text, nullable=False)

    # Contexto
    intent = Column(String(100), nullable=True)  # shopping, menu, waste, general, etc.
    confidence = Column(Float, default=0)  # Confianza en la detección de intención

    # Metadata
    provider = Column(String(50), nullable=True)  # "openai", "anthropic", "local"
    tokens_used = Column(Integer, default=0)

    # Relación
    conversation = relationship("AIConversation", back_populates="messages")

    def __repr__(self) -> str:
        return f"<AIMessage(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"
