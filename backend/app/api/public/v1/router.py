from fastapi import APIRouter
from app.api.public.v1 import health
from app.api.public.v1 import auth

router = APIRouter(prefix="/api/public/v1")

router.include_router(auth.router)
router.include_router(health.router)
