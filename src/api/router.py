from fastapi import APIRouter

from .endpoints.health import router as health_router
from .endpoints.technologies import router as technologies_router

router = APIRouter()

router.include_router(health_router)
router.include_router(technologies_router)