"""Catálogo de Productos. Relación de N:M de productos con sus ingredientes y relación con Usuarios (Proveedores)."""

from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from pydantic import model_validator
import re


# TABLA INTERMEDIA (MUCHOS A MUCHOS)
class ProductIngredientLink(SQLModel, table=True):
    """Tabla pivote para unir Productos con sus Ingredientes/Atributos."""

    __tablename__ = "product_ingredient_link"

    product_id: int = Field(foreign_key="products.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredients.id", primary_key=True)


# CATÁLOGO DE ATRIBUTOS / INGREDIENTES
class IngredientBase(SQLModel):
    name: str = Field(unique=True, index=True, max_length=100)


class Ingredient(IngredientBase, table=True):
    """Tabla maestra de características."""

    __tablename__ = "ingredients"

    id: Optional[int] = Field(default=None, primary_key=True)

    products: List["Products"] = Relationship(
        back_populates="ingredients", link_model=ProductIngredientLink
    )


# PRODUCTOS
class Coupons(SQLModel, table=True):
    """Cupones de Desuento a nuestros clientes."""

    __tablename__ = "coupons"
    id: Optional[int] = Field(default=None, primary_key=True)


class __ProductBase(SQLModel):
    name: str = Field(index=True, max_length=255)
    description: Optional[str] = Field(default=None)
    price: Decimal = Field(default=0, max_digits=10, decimal_places=2, ge=0)

    # EL CAMBIO CLAVE: Ahora el proveedor es un Usuario de tu tabla 'users'
    provider_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="ID del usuario que vende este producto",
    )

    coupon_id: Optional[int] = Field(default=None, foreign_key="coupons.id")

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

    ingredients: List[Ingredient] = Relationship(
        back_populates="products", link_model=ProductIngredientLink
    )


# ENDPOINTS (REQUESTS & RESPONSES)
class ProductGet(__ProductBase):
    """Respuesta de la API."""

    id: int
    created_at: datetime
    ingredients: List[IngredientBase]


class ProductPost(SQLModel):
    """Payload de creación por parte del cliente."""

    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    price: Decimal = Field(default=0, max_digits=10, decimal_places=2, ge=0)
    coupon_id: Optional[int] = Field(default=None)

    ingredient_ids: List[int] = Field(default=[])
