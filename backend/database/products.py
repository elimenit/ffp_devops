"""Gestion de los usuarios en la Base de Datos"""
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from typing import List
from dependencies.dbsession import get_session
from schemas.products import ProductGet, ProductPost, ProductPacth
from schemas.products import Products
from schemas.users import Users


class DBProducts:
    """Entidad que manipula la BD de los productos de forma segura por request"""

    def __init__(self, session: AsyncSession = Depends(get_session)):
        """Crea automaticamente la sesiones a la Base de Datos."""
        self.session = session

    def __generate_tokens(self, name: str, category: str) -> str:
        return f"{name} {category}".lower()

    async def add(self, product: ProductPost, user_id: int) -> ProductGet:
        """Agrega un usuario a la BD de forma asíncrona"""
        # Verificamos que el usuario exista
        user: Users | None = await self.session.get(Users, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado!"
            )

        # Contamos la cantidad de Productos del usuario
        result = await self.session.execute(
            select(func.count(Products.id)).where(Products.user_id == user_id)
        )
        current_count = result.one()

        # validamos el limite de products
        if current_count >= user.role.product_limit:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"limite alcanzado{user.role.product_limit}: tu rol: '{user.role.value}'",
            )

        db_product: Products = Products.model_validate(
            product, update={"user_id": user_id}
        )
        db_product.search_tokens = self.__generate_tokens(
            db_product.name, db_product.category
        )

        db_product = Products.model_validate(product)
        self.session.add(db_product)

        await self.session.commit()
        await self.session.refresh(db_product)

        return ProductGet.model_validate(db_product)

    async def get(self, user_id: int, product_id) -> ProductGet:
        """Obtiene solo un Product"""
        statement = select(Products).where(
            Products.id == product_id, Products.user_id == user_id
        )

        result = await self.session.execute(statement)
        product = result.first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        return UserGet.model_validate(user)

    async def update(
        self, user_id: int, product_id: int, product_update: ProductPacth
    ) -> ProductGet:
        """Actualiza los campos necesarios de un Product"""

        statement = select(Products).where(
            Products.id == product_id, Products.user_id == user_id
        )

        result = await self.session.execute(statement)
        product = result.first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        for k, v in user_update.model_dump(exclude_unset=True).items():
            setattr(product, k, v)

        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return ProductGet.model_validate(product)

    async def filters(self, filters: UserFilters) -> List[UserGet]:
        """Obtiene mas de un Usuario aplicando filtros"""
        query = self.__build_list_query(filters)

        offset_val = getattr(filters, "offset", 0)
        limit_val = getattr(filters, "limit", 100)
        query = query.offset(offset_val).limit(limit_val)

        result = await self.session.execute(query)
        users = result.scalars().all()
        return [UserGet.model_validate(u) for u in users]

    async def delete(self, user_id: int, product_id) -> ProductGet:
        """Elimina un producto de un usuario"""

        statement = select(Products).where(
            Products.id == product_id, Products.user_id == user_id
        )

        result = await self.session.execute(statement)
        product = result.first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )

        await self.session.delete(product)
        await self.session.commit()

        return ProductGet.model_validate(product)

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
