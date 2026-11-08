"""Aplicacion Principal"""
from contextlib import asynccontextmanager
from fastapi import FastAPI


from dependencies.dbsession import init_db, engine
from routers.routes import router

from constants import valida_entorn_variable

# Models
from schemas.orders import StatusOrder, Orders
from schemas.payments import ProvidersPayments, Payment
from schemas.products import ProductIngredientLink, Ingredient, Products, Coupons
from schemas.users import Users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inizializa la Base de Datos por primera ves.\n"""

    valida_entorn_variable()
    await init_db()

    yield

    await engine.dispose()


app: FastAPI = FastAPI(title="Goats for everithing", lifespan=lifespan)
app.include_router(router)


@app.get("/")
def main():
    """Funcion principal"""
    return {"message": "Hola Mundo"}
