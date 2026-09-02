"""
FOODARA AI - Shopping Models
Modelos para listas de compra y productos.
"""

from sqlalchemy import String, Float, Integer, Column, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from app.database.base import Base, IDMixin, TimeStampMixin


class Product(Base, IDMixin, TimeStampMixin):
    """
    Producto en el sistema FOODARA.
    Representa un producto comercial específico.
    """
    __tablename__ = "products"

    # Identificación
    name = Column(String(255), index=True, nullable=False)
    brand = Column(String(100), nullable=True)
    category = Column(String(100), index=True, nullable=False)
    barcode = Column(String(50), unique=True, nullable=True)

    # Información de precio
    price_ars = Column(Float, nullable=True)
    supermarket = Column(String(100), nullable=True)

    # Información del producto
    quantity = Column(Float, nullable=True)
    unit = Column(String(50), nullable=True)

    # Descripción y notas
    description = Column(Text, nullable=True)

    # Items en listas
    shopping_list_items = relationship("ShoppingListItem", back_populates="product")
    purchase_items = relationship("Purchase", back_populates="product")

    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name={self.name}, brand={self.brand})>"


class ShoppingList(Base, IDMixin, TimeStampMixin):
    """
    Lista de compras del usuario.
    Un usuario puede tener múltiples listas.
    """
    __tablename__ = "shopping_lists"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)

    # Relaciones
    user = relationship("User", back_populates="shopping_lists")
    items = relationship("ShoppingListItem", back_populates="shopping_list", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<ShoppingList(id={self.id}, user_id={self.user_id}, name={self.name})>"


class ShoppingListItem(Base, IDMixin, TimeStampMixin):
    """
    Item en una lista de compras.
    Representa un producto que el usuario quiere comprar.
    """
    __tablename__ = "shopping_list_items"

    shopping_list_id = Column(Integer, ForeignKey("shopping_lists.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    # Información del item
    product_name = Column(String(255), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(50), nullable=False)

    # Seguimiento
    is_purchased = Column(Boolean, default=False)
    price_estimate_ars = Column(Float, nullable=True)

    notes = Column(Text, nullable=True)

    # Relaciones
    shopping_list = relationship("ShoppingList", back_populates="items")
    product = relationship("Product", back_populates="shopping_list_items")

    def __repr__(self) -> str:
        return f"<ShoppingListItem(id={self.id}, product_name={self.product_name}, quantity={self.quantity})>"
