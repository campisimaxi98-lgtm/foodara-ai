"""
FOODARA AI - Purchase Models
Modelos para compras realizadas.
"""

from sqlalchemy import String, Float, Integer, Column, ForeignKey, DateTime

from app.database.base import Base, IDMixin, TimeStampMixin, utcnow


class Purchase(Base, IDMixin, TimeStampMixin):
    """
    Compra realizada por el usuario.
    Registro de una transacción de compra.
    """
    __tablename__ = "purchases"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)
    price_ars = Column(Float, nullable=False)

    supermarket = Column(String(100), nullable=True)
    purchase_date = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    # Relaciones
    user = relationship("User", back_populates="purchases")
    product = relationship("Product", back_populates="purchase_items")

    def __repr__(self) -> str:
        return f"<Purchase(id={self.id}, user_id={self.user_id}, price={self.price_ars})>"
