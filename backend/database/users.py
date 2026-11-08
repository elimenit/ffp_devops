"""Gestion de los usuarios en la Base de Datos"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from dependencies.dbsession import get_session
from schemas.users import UserPost, UserGet, UserPatch, UserFilters
from schemas.users import Users


class DBUsers:
    """Entidad que manipula la BD de users de forma segura por request"""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        """Crea automaticamente la sesiones a la Base de Datos."""
        self.session = session

    async def add(self, user: UserPost) -> UserGet:
        """Agrega un usuario a la BD de forma asíncrona"""

        result = await self.session.execute(
            select(Users).where(Users.email == user.email)
        )
        existing = result.scalars().first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email ya existe"
            )

        new_user = Users.model_validate(user)
        self.session.add(new_user)

        await self.session.commit()
        await self.session.refresh(new_user)

        return UserGet.model_validate(new_user)

    async def get(self, user_id: int) -> UserGet:
        """Obtiene solo un Usuario"""
        user = await self.session.get(Users, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserGet.model_validate(user)

    async def update(self, user_id: int, user_update: UserPatch) -> UserGet:
        """Actualiza los campos necesarios de un usuario"""
        user = await self.session.get(Users, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        for k, v in user_update.model_dump(exclude_unset=True).items():
            setattr(user, k, v)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserGet.model_validate(user)

    async def filters(self, filters: UserFilters) -> List[UserGet]:
        """Obtiene mas de un Usuario aplicando filtros"""
        query = self.__build_list_query(filters)

        offset_val = getattr(filters, "offset", 0)
        limit_val = getattr(filters, "limit", 100)
        query = query.offset(offset_val).limit(limit_val)

        result = await self.session.execute(query)
        users = result.scalars().all()
        return [UserGet.model_validate(u) for u in users]

    async def delete(self, user_id: int) -> UserGet:
        """Elimina un usuario por su ID"""
        user = await self.session.get(Users, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
            )

        await self.session.delete(user)
        await self.session.commit()

        return UserGet.model_validate(user)

    def __escape_sql_wildcards(self, text: str) -> str:
        """Escapa los parametros ingresados por el usuario para evitar inyecciones SQL"""
        return text.replace("%", "\\%").replace("_", "\\_").replace("'", "\\'")

    def __build_list_query(self, filters: UserFilters):
        """Construye la query con los filtros diferentes de None"""

        query = select(Users)

        if not filters:
            return query

        filter_dict = filters.model_dump(exclude={"limit", "offset"}, exclude_none=True)
        for key, val in filter_dict.items():
            if isinstance(val, str):
                safe_val = self.__escape_sql_wildcards(val)
                query = query.where(getattr(User, key).ilike(f"%{safe_val}%"))
            else:
                query = query.where(getattr(User, key) == val)
        return query
