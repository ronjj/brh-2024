from fastapi import APIRouter, HTTPException
from app.calendar_utils import get_calendar_service, get_free_busy, find_available_gym_slots, get_random_workout, EST_TIMEZONE
from app.dining_utils import get_eateries
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

# @router.get("/available-slots")
# async def get_available_slots(date: date):
#     try:
#         service = get_calendar_service()
#         free_slots = get_free_slots(service, date)
#         return { "available_slots": free_slots }
#     except HttpError as error:
#         raise HTTPException(status_code=500, detail=str(error))

@router.post("/create-event")
async def create_event(event: dict):
    try:
        service = get_calendar_service()
        created_event = service.events().insert(calendarId='primary', body=event).execute()
        return created_event
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))

@router.get("/get-gym-assignment")
async def get_gym_assignment(gym: str, date: date, create_event: bool = False):
    try:
        service = get_calendar_service()
        busy_slots = get_free_busy(service, date)
        available_slots = find_available_gym_slots(gym, date, busy_slots)
        
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
                
                if create_event:
                    service.events().insert(calendarId='primary', body=event).execute()
                
                return {
                    "available_slots": available_slots,
                    "event": event
                }
            else:
                return {"available_slots": available_slots, "created_event": None, "message": f"No slot available for a {workout_duration} workout"}
        else:
            return {"available_slots": [], "created_event": None}
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid gym name: {gym}")


# Dining


@router.get("/suggest-meals")
async def suggest_meals(date: date, create_event: bool = False):
    try:
        service = get_calendar_service()
        busy_slots = get_free_busy(service, date)
        eateries = await get_eateries()
        
        # Define meal times
        meal_times = [
            {"name": "Breakfast", "start": datetime.combine(date, datetime.min.time().replace(hour=7)), "duration": timedelta(minutes=30)},
            {"name": "Lunch", "start": datetime.combine(date, datetime.min.time().replace(hour=12)), "duration": timedelta(minutes=45)},
            {"name": "Dinner", "start": datetime.combine(date, datetime.min.time().replace(hour=18)), "duration": timedelta(minutes=60)}
        ]
        
        suggested_meals = []
        
        for meal in meal_times:
            # Find a free slot for the meal
            meal_slot = find_free_slot(busy_slots, meal["start"], meal["duration"])
            
            if meal_slot:
                # Find an open eatery for this meal time
                eatery = find_open_eatery(eateries, date, meal_slot["start"].time(), meal_slot["end"].time())
                
                if eatery:
                    event_summary = f"{meal['name']} at {eatery['Name']}"
                    
                    event = {
                        'summary': event_summary,
                        'location': eatery['Location'],
                        'description': f"Suggested {meal['name']} at {eatery['Name']}",
                        'start': {
                            'dateTime': meal_slot["start"].isoformat(),
                            'timeZone': 'America/New_York',
                        },
                        'end': {
                            'dateTime': meal_slot["end"].isoformat(),
                            'timeZone': 'America/New_York',
                        },
                    }
                    
                    if create_event:
                        service.events().insert(calendarId='primary', body=event).execute()
                    
                    suggested_meals.append(event)
        
        return suggested_meals
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))

def find_free_slot(busy_slots, start_time, duration):
    # Make start_time timezone-aware
    start_time = start_time.replace(tzinfo=EST_TIMEZONE)  # Adjust to your desired timezone
    end_time = start_time + duration
    for slot in busy_slots:
        slot_start = datetime.fromisoformat(slot['start']).replace(tzinfo=EST_TIMEZONE)  # Adjust to your desired timezone
        slot_end = datetime.fromisoformat(slot['end']).replace(tzinfo=EST_TIMEZONE)  # Adjust to your desired timezone
        if start_time >= slot_end or end_time <= slot_start:
            continue
        if start_time < slot_start:
            end_time = min(end_time, slot_start)
        else:
            start_time = max(start_time, slot_end)
    
    if end_time - start_time >= duration:
        return {"start": start_time, "end": end_time}
    return None

def find_open_eatery(eateries, date, start_time, end_time):
    day_name = date.strftime("%A")
    for eatery in eateries:
        for eatery_date in eatery['Dates']:
            if eatery_date['Date'] == str(date):
                for event in eatery_date['Events']:
                    # Change the format to accommodate "am"/"pm"
                    event_start = datetime.strptime(event['Start'], "%I:%M%p").time()
                    event_end = datetime.strptime(event['End'], "%I:%M%p").time()
                    if event_start <= start_time and event_end >= end_time:
                        return eatery
    return None