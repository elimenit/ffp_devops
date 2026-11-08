"""Endpoint para los usuarios.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body, Query
from schemas.users import UserPost, UserGet, UserFilters, UserPatch

from database.users import DBUsers

router_user = APIRouter(tags=["users"])

DBUsersDep = Annotated[DBUsers, Depends(DBUsers)]


# Users
@router_user.post("/", response_model=UserGet, status_code=201)
async def create_user(db: DBUsersDep, user: UserPost = Body()):
    return await db.add(user)


@router_user.get("/{user_id}", response_model=UserGet, status_code=200)
async def get_user(db: DBUsersDep, user_id: int = Path(gt=0)):
    return await db.get(user_id)


@router_user.get("/", response_model=list[UserGet], status_code=200)
async def filters_users(db: DBUsersDep, filters: UserFilters = Query()):
    return await db.filters(filters=filters)


@router_user.patch("/{user_id}", response_model=UserGet)
async def update_user(db: DBUsersDep, user_id: int = Path(), user: UserPatch = Body()):
    return await db.update(user_id, user)


@router_user.delete("/{user_id}", response_model=UserGet, status_code=200)
async def delete_user(db: DBUsersDep, user_id: int = Path(ge=0)):
    return await db.delete(user_id)
