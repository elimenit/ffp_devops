"""Aplicacion Principal - Frontend
"""
## App
from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Dependencies Templates
from dependencies.templates import get_templates
from routers.routers import endpoints

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(path="/", response_class=HTMLResponse)
async def read_root(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Endpoint raiz"""
    context = {"title": "Inicio - FastAPI"}
    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )


app.include_router(router=endpoints)
