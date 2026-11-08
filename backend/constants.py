"""Configuracion de las variable de entorno.\n
"""
import os

from dotenv import load_dotenv


load_dotenv()
DATABASE_URL: str = os.getenv("DATABASE_URL")


def _enviroment_variables_exists(variable: str):
    """Valida la existencia de las variables de entorno"""
    if not variable:
        raise Exception("No existe la variable de entorno DATABASE_URL: ", DATABASE_URL)


def valida_entorn_variable():
    """Valida la existencia de las variables de entorno.\n"""
    _enviroment_variables_exists(DATABASE_URL)
