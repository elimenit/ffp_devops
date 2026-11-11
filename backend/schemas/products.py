"""Catálogo de Productos. Relación de N:M de productos con sus ingredientes y relación con Usuarios (Proveedores)."""

from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Index
from pydantic import model_validator
import re


# PRODUCTOS
class Coupons(SQLModel, table=True):
    """Cupones de Desuento a nuestros clientes."""

    __tablename__ = "coupons"
    id: Optional[int] = Field(default=None, primary_key=True)


class __ProductBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None)
    price: float = Field(default=0, max_digits=10, decimal_places=2, ge=0)
    # category funcionara como un strings de etiquetas
    category: str = Field(index=True)
    coupon_id: Optional[int] = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def sanitize_all_string_fields(cls, data: dict) -> dict:
        """Limpia los parametros recibidos por el usuario"""

        if not isinstance(data, dict):
            return data

        for field_name, value in data.items():
            if isinstance(value, str):
                if "email" in field_name.lower() or "@" in value:
                    data[field_name] = re.sub(r"['\"\-;=<>]", "", value).strip()
                else:
                    data[field_name] = re.sub(r"['\"\-;=<>/]", "", value).strip()
        return data


class Products(__ProductBase, table=True):
    """Entidad Producto en BD."""

    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="ID del usuario que vende este producto",
    )
    search_tokens: str = Field(default="")
    __table_args__ = (
        Index(
            "ix_product_search_tokens_gin",
            "search_tokens",
            postgresql_using="gin",
            postgresql_ops={"search_tokens": "gin_trgm_ops"},
            postgresql_with={"fastupdate": "on"},
        ),
    )


# ENDPOINTS (REQUESTS & RESPONSES)
class ProductGet(__ProductBase):
    """Respuesta de la API."""

    id: int
    user_id: int
    created_at: datetime
    ingredients: List[IngredientBase]


class ProductPost(__ProductBase):
    """Payload de creación por parte del cliente."""

    pass


class ProductPacth(SQLModel):
    name: Optional[str] = Field(default=None, index=True, max_length=255)
    description: Optional[str] = Field(max_length=500)
    price: Optional[float] = Field(default=None, decimal_places=2, ge=0, max_digits=10)
    category: Optional[str] = None


class ProductFilters(__ProductBase):
    """Filtros de Productos"""

    search: Optional[str] = Field(default=None, ge=5, le=255)
    name: Optional[str] = Field(default=None, ge=5, le=255)
    min_price: Optional[float] = Field(default=None, ge=0)
    max_price: Optional[float] = Field(default=None)
    user_id: Optional[int] = None
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, le=50)

    @property
    def reverse_range_price(self):
        """Invierte los precios si price_min >  price_max"""

        if self.min_price and self.max_price:
            if self.min_price > self.max_price:
                self.min_price, self.max_price = self.max_price, self.min_price

        return self
