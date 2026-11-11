"""Administración de usuarios y roles."""
from enum import Enum
from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, model_validator
import re


class __UserBase(SQLModel):
    """Entidad Base de usuarios."""

    email: EmailStr = Field(unique=True, index=True, min_length=5, max_length=250)
    username: str = Field(index=True, min_length=5, max_length=50)

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


# BASE DE DATOS
class UserRole(str, Enum):
    """Roles que puede tener cualquier Usuario"""

    CLIENT: str = "CLIENT"
    PROVIDER: str = "PROVIDER"
    PARTNER: str = "PARTNER"
    SPONSOR: str = "SPONSOR"
    ADMIN: str = "ADMIN"

    @property
    def product_limit(self) -> int:
        limits = {
            self.CLIENT: 10,
            self.PROVIDER: 100,
            self.PARTNER: 500,
            self.SPONSOR: 1000,
            self.ADMIN: 2000,
        }
        return limits[self]


class Users(__UserBase, table=True):
    """Usuario en la base de datos."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, ge=0, le=1_000_000)
    password: str = Field(nullable=False, min_length=8, max_length=255)
    is_active: bool = Field(default=True)
    role: UserRole = Field(UserRole.CLIENT, nullable=False, min_length=1, max_length=50)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


# ENDPOINTS (REQUESTS & RESPONSES)
class UserGet(__UserBase):
    """La entidad usuario a devolver (¡NUNCA expone el password!)."""

    id: int
    is_active: bool
    created_at: datetime


class UserPost(__UserBase):
    """Payload para registrar usuarios. Protegido contra asignación masiva."""

    password: str = Field(nullable=False, min_length=14, max_length=128)


class UserPatch(__UserBase):
    """Payload para peticiones PATCH. Todo es opcional."""

    email: Optional[EmailStr] = Field(default=None, min_length=5, max_length=255)
    username: Optional[str] = Field(default=None, min_length=5, max_length=50)
    role_id: Optional[int] = Field(default=None, ge=1, le=1_000_000)
    is_active: Optional[bool] = Field(default=True)


class UserFilters(__UserBase):
    """Filtros de Usuarios."""

    email: Optional[str] = Field(default=None, ge=5, le=255)
    username: Optional[str] = Field(default=None, min_length=11)
    role_id: Optional[int] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, le=50)
