"""Dependencia para la importacion de Plantillas de FastAPI con Jinja2
"""
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


def get_templates() -> Jinja2Templates:
    return templates
