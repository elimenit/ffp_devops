"""Esquemas de Pagos"""

from typing import Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field


# PROVEEDORES DE PAGOS
class __ProvidersPaymentsBase(SQLModel):
    """Atributos comunes del proveedor de pagos."""

    name: str = Field(max_length=50, unique=True, index=True)


class ProvidersPayments(__ProvidersPaymentsBase, table=True):
    """Tabla de Proveedores de Pagos."""

    __tablename__ = "providers_payments"

    id: Optional[int] = Field(default=None, primary_key=True)


# PAGOS (BASE Y DB)
class __PaymentBase(SQLModel):
    """Entidad Base de Pagos."""

    mount: int = Field(
        gt=0,
        description="Monto pagado. Idealmente en centavos para evitar errores de coma flotante.",
    )

    user_id: int = Field(foreign_key="users.id", index=True)
    order_id: int = Field(
        foreign_key="orders.id", index=True, unique=True
    )  # Un pago por orden suele ser la regla
    provider_payment_id: int = Field(foreign_key="providers_payments.id", index=True)


class Payment(__PaymentBase, table=True):
    """Entidad de pagos en la base de datos."""

    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )


# ENDPOINTS (REQUESTS & RESPONSES)
class PaymentPost(__PaymentBase):
    """Payload para registrar un pago."""

    pass


class PaymentGet(__PaymentBase):
    """Entidad a devolver en los endpoints."""

    id: int
    created_at: datetime


class PaymentFilters(SQLModel):
    """Filtros estrictos de busqueda de Pagos (Query Parameters).
    SIN table=True para evitar errores de base de datos."""

    user_id: Optional[int] = Field(default=None, description="Filtrar por usuario")
    order_id: Optional[int] = Field(default=None, description="Filtrar por orden")
    provider_payment_id: Optional[int] = Field(
        default=None, description="Filtrar por proveedor"
    )

    min_mount: Optional[int] = Field(default=None, ge=0)
    max_mount: Optional[int] = Field(default=None, ge=0)

    offset: int = Field(default=0, ge=0, description="Número de registros a omitir")
    limit: int = Field(
        default=20, le=100, description="Máximo 100 registros por consulta"
    )
