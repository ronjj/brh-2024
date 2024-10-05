from fastapi import APIRouter, HTTPException
from app.calendar_utils import get_calendar_service

router = APIRouter()

@router.get("/events")
async def get_events():
    try:
        service = get_calendar_service()
        events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])
        return events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/events")
async def create_event(event: dict):
    try:
        service = get_calendar_service()
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))