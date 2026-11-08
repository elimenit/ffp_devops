from fastapi import APIRouter
from routers.auth import auth_router
from routers.users import users_router

endpoints = APIRouter()
endpoints.include_router(auth_router)
endpoints.include_router(users_router)
