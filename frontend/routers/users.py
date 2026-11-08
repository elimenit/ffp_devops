"""Users Frontend
"""
from fastapi import APIRouter, Query, Body, Path, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from resources.user import post_create_user
from dependencies.templates import get_templates
from schemas.user import UserPost, User

users_router: APIRouter = APIRouter(prefix="/users")

list_users: list[User] = []


@users_router.get(path="/", response_class=HTMLResponse)
async def show_user(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Muestra los usuarios"""
    context: dict = {}
    return templates.TemplateResponse(
        request=request, name="pages/users.html", context=context
    )


@users_router.get(path="/", response_class=HTMLResponse)
async def show_user(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    id: int = Path(),
):
    """Muestra un Usuario"""
    user: User
    i = 0
    is_found: bool = False
    while i < len(list_users) and not is_found:
        if list_users[i].id == id:
            is_found = True
        else:
            i += 1

    user = list_users[id]
    return templates.TemplateResponse(
        request=request, name="user.html", context=user.model_dump()
    )


@users_router.post(path="/")
async def create_user(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    user: UserPost = Body(),
):
    print(user.model_dump())
    new_user: dict = {"id": 3, "name": "carlos", "email": "ex@gmail.com"}

    return templates.TemplateResponse(
        request=request, name="pages/users.html", context=new_user
    )
