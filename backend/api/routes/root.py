from fastapi import APIRouter
from core.config import settings

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }
