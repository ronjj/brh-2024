from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.services.calendar_service import CalendarService

router = APIRouter()

@router.get("/events")
async def get_events(current_user: dict = Depends(get_current_user)):
    calendar_service = CalendarService(current_user)
    return await calendar_service.get_events()

@router.post("/events")
async def create_event(event_data: dict, current_user: dict = Depends(get_current_user)):
    calendar_service = CalendarService(current_user)
    return await calendar_service.create_event(event_data)