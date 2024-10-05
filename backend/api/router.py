from fastapi import APIRouter
from app.api.endpoints import auth, calendar

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])