"""Users Frontend
"""
from fastapi import APIRouter, Query, Body, Path, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from resources.user import post_create_user
from dependencies.templates import get_templates

auth_router: APIRouter = APIRouter(prefix="/auth")


@auth_router.get(path="/login", response_class=HTMLResponse)
async def template_login(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Muestra los usuarios"""
    context: dict = {}
    return templates.TemplateResponse(
        request=request, name="login.html", context=context
    )


@auth_router.get(path="/signup", response_class=HTMLResponse)
async def template_signup(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Muestra los usuarios"""
    context: dict = {}
    return templates.TemplateResponse(
        request=request, name="signup.html", context=context
    )


@auth_router.get(path="/verification", response_class=HTMLResponse)
async def templaate_verification(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Verificacion para la creacion de un usuario"""
    context: dict = {}
    return templates.TemplateResponse(request=request, name="verification.html")


@auth_router.post(path="/saludar")
async def saludar(
    request: Request,
    name: str = Body(),
    templates: Jinja2Templates = Depends(get_templates),
):
    context: dict = {"name": name}
    print(name)
    return templates.TemplateResponse(
        request=request, name="partials/users/invitation.html", context=context
    )
