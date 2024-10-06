from fastapi import APIRouter, HTTPException
from app.calendar_utils import get_calendar_service, get_free_busy, find_available_slots, get_random_workout
from googleapiclient.errors import HttpError
from datetime import datetime, date, timedelta

router = APIRouter()

@router.get("/events")
async def get_events():
    try:
        service = get_calendar_service()
        events = get_upcoming_events(service)
        return [{"start": event["start"].get("dateTime", event["start"].get("date")), "summary": event["summary"]} for event in events]
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.post("/events")
async def create_event(event: dict):
    try:
        service = get_calendar_service()
        event = service.events().insert(calendarId='primary', body=event).execute()
        return event
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.get("/available-gym-slots")
async def get_available_gym_slots(gym: str, date: date):
    try:
        service = get_calendar_service()
        busy_slots = get_free_busy(service, date)
        available_slots = find_available_slots(gym, date, busy_slots)
        
        # Define workout duration
        workout_duration = timedelta(hours=1)
        
        if available_slots:
            # Find the first slot with enough time for the workout
            first_available_slot = next(
                (slot for slot in available_slots if (
                    datetime.combine(date, slot["end"]) - datetime.combine(date, slot["start"])
                ) >= workout_duration),
                None
            )
            
            if first_available_slot:
                workout_type = get_random_workout()
                event_summary = f"{workout_type} Workout at {gym}"
                
                start_time = datetime.combine(date, first_available_slot["start"])
                end_time = start_time + workout_duration
                
                event = {
                    'summary': event_summary,
                    'location': gym,
                    'description': f'Scheduled {workout_type} workout at {gym}',
                    'start': {
                        'dateTime': start_time.isoformat(),
                        'timeZone': 'America/New_York',
                    },
                    'end': {
                        'dateTime': end_time.isoformat(),
                        'timeZone': 'America/New_York',
                    },
                }
                
                created_event = service.events().insert(calendarId='primary', body=event).execute()
                
                return {
                    "available_slots": available_slots,
                    "created_event": {
                        "summary": created_event["summary"],
                        "start": created_event["start"]["dateTime"],
                        "end": created_event["end"]["dateTime"],
                    }
                }
            else:
                return {"available_slots": available_slots, "created_event": None, "message": f"No slot available for a {workout_duration} workout"}
        else:
            return {"available_slots": [], "created_event": None}
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid gym name: {gym}")