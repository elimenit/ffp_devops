"""Gestión de Pedidos (Orders)."""

from typing import Optional
from decimal import Decimal
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from enum import Enum


# ESTADOS DE ORDEN
class StatusOrder(str, Enum):
    """Catálogo de estados de una orden (ej: 'PENDIENTE', 'ENVIADO')."""

    PENDIENTE: str = "PENDIENTE"
    PREPARACION: str = "PREPARACION"
    ENVIADO: str = "ENVIADO"


# ORDENES (PEDIDOS)
class __OrderBase(SQLModel):
    """Datos comunes del pedido."""

    address: str = Field(max_length=255)

    status: StatusOrder = Field(StatusOrder.PENDIENTE, nullable=False)
    product_id: int = Field(foreign_key="products.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    stock: int = Field(gt=0, description="Cantidad de productos comprados")
    mount: Decimal = Field(max_digits=12, decimal_places=2, ge=0)


class Orders(__OrderBase, table=True):
    """Tabla de Órdenes en la Base de Datos."""

    __tablename__ = "orders"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )


# ENDPOINTS (REQUESTS & RESPONSES)
class OrderPost(SQLModel):
    """Lo que el cliente envía. El servidor calcula el `mount` y `status_id`."""

    address: str = Field(max_length=255)
    product_id: int
    stock: int = Field(gt=0)


class OrderGet(__OrderBase):
    id: int
    created_at: datetime
