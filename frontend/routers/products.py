"""Users Frontend
"""
from fastapi import APIRouter, Query, Body, Path, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from resources.user import post_create_user
from dependencies.templates import get_templates

products_router: APIRouter = APIRouter(prefix="/users")


@products_router.get(path="/", response_model=HTMLResponse)
async def template_products(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Muestra los productos"""
    context: dict = {}
    return templates.TemplateResponse(
        request=request, name="products.html", context=context
    )


@products_router.get(path="/", response_model=HTMLResponse)
async def template_product(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Muestra un solo producto."""
    context: dict = {}
    return templates.TemplateResponse(
        request=request, name="product.html", context=context
    )
