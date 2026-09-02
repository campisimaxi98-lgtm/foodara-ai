"""
FOODARA AI - Receipt Models
Modelos para lectura y análisis de tickets.
"""

from sqlalchemy import String, Float, Integer, Column, ForeignKey, DateTime, Text

from app.database.base import Base, IDMixin, TimeStampMixin, utcnow


class Receipt(Base, IDMixin, TimeStampMixin):
    """
    Ticket de compra procesado.
    Resultado de analizar una foto de ticket.
    """
    __tablename__ = "receipts"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Información del ticket
    store_name = Column(String(255), nullable=True)
    receipt_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Totales
    subtotal_ars = Column(Float, default=0)
    tax_ars = Column(Float, default=0)
    total_ars = Column(Float, default=0)

    # Procesamiento
    confidence = Column(Float, default=0)  # Confianza en el OCR/reconocimiento
    raw_data = Column(Text, nullable=True)  # JSON con datos crudos

    # Relaciones
    user = relationship("User", back_populates="receipts")
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Receipt(id={self.id}, user_id={self.user_id}, total={self.total_ars})>"


class ReceiptItem(Base, IDMixin, TimeStampMixin):
    """
    Item individual en un ticket.
    Producto comprado en una transacción.
    """
    __tablename__ = "receipt_items"

    receipt_id = Column(Integer, ForeignKey("receipts.id"), nullable=False)

    # Información del producto
    product_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=True)

    # Precios
    unit_price_ars = Column(Float, nullable=True)
    total_price_ars = Column(Float, nullable=False)

    # Relación
    receipt = relationship("Receipt", back_populates="items")

    def __repr__(self) -> str:
        return f"<ReceiptItem(id={self.id}, product_name={self.product_name})>"
