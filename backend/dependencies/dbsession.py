"""Archivo que genera la creacion de la Base de Datos y genera las sessiones.
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from constants import DATABASE_URL

# Models
from schemas.orders import StatusOrder, Orders
from schemas.payments import ProvidersPayments, Payment
from schemas.products import ProductIngredientLink, Ingredient, Products, Coupons
from schemas.users import Users

engine = create_async_engine(DATABASE_URL, echo=True)


async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print("[-] Error al conectar o crear la BD:", e)


# Esta es la única dependencia real de BD que necesitas
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
