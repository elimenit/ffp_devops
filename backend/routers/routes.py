"""Agrupa Los ApiRouters para que sea esacalable
"""
from fastapi import APIRouter
from routers.users import router_user

router = APIRouter()
router.include_router(router=router_user, prefix="/users")
# api_router.include_router(auth.router, prefix="/auth")
# api_router.include_router(reviews.router, prefix="/reviews")
# api_router.include_router(products.router, prefix="/products")
# api_router.include_router(payments.router, prefix="/payments")
# api_router.include_router(deliveries.router, prefix="/deliveries")
