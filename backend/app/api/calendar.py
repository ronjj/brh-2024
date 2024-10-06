from typing import Tuple
from fastapi import APIRouter, HTTPException
from app.calendar_utils import get_calendar_service, get_free_busy, find_available_gym_slots, get_random_workout, EST_TIMEZONE
from app.dining_utils import get_eateries
from googleapiclient.errors import HttpError
from datetime import datetime, date, timedelta
import json

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

@router.get("/suggest-workout")
async def suggest_workout(gym: str, date: date, create_event: bool = False):
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

# Update the load_meals_data function to return the date range
def load_meals_data() -> Tuple[dict, date, date]:
    with open('meals_data.json', 'r') as file:
        meals_data = json.load(file)
    
    # Convert string dates to date objects and find min and max
    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in meals_data.keys()]
    start_date = min(dates)
    end_date = max(dates)
    
    return meals_data, start_date, end_date

@router.post("/suggest-meals")
async def suggest_meals():
    try:
        # Load meals data and get the date range
        meals_data, start_date, end_date = load_meals_data()
        
        service = get_calendar_service()
        created_events = []
        
        current_date = start_date
        while current_date <= end_date:
            # Check if the date exists in the meals data
            if str(current_date) in meals_data:
                # Get meals for the current date
                meals = meals_data[str(current_date)]["meals"]
                
                for meal in meals:
                    details = meal["details"]
                    start_time_str = details["Start"]
                    end_time_str = details["End"]
                    
                    # Define meal duration based on meal type
                    if details["time"] == "Breakfast":
                        meal_duration = timedelta(minutes=30)
                    elif details["time"] in ["Lunch", "Late Lunch"]:
                        meal_duration = timedelta(minutes=45)
                    elif details["time"] in ["Dinner", "Late Dinner"]:
                        meal_duration = timedelta(minutes=60)
                    else:
                        continue  # Skip if the meal type is not recognized
                    
                    # Parse the start time to find a free slot
                    start_time = datetime.strptime(start_time_str, "%I:%M%p").replace(year=current_date.year, month=current_date.month, day=current_date.day, tzinfo=EST_TIMEZONE)
                    end_time = datetime.strptime(end_time_str, "%I:%M%p").replace(year=current_date.year, month=current_date.month, day=current_date.day, tzinfo=EST_TIMEZONE)
                    
                    # Get busy slots for the day
                    busy_slots = get_free_busy(service, current_date)
                    
                    # Find a free slot for the meal
                    meal_slot = find_free_slot(busy_slots, start_time, meal_duration)
                    
                    if meal_slot:
                        # Prepare the macro information
                        best_combination = details.get("Best combination", {})
                        macro_info = []
                        for food, values in best_combination.items():
                            macro_info.append(f"{food}: {values[1]} calories, {values[2]}g protein, {values[3]}g carbs, {values[4]}g fats")
                        
                        # Create a detailed description
                        description = f"Suggested meal at {details['eatery']}.\n" + "\n".join(macro_info)
                        
                        event = {
                            'summary': f"{details['time']} at {details['eatery']}",
                            'location': details['eatery'],
                            'description': description,
                            'start': {
                                'dateTime': meal_slot["start"].isoformat(),
                                'timeZone': 'America/New_York',
                            },
                            'end': {
                                'dateTime': meal_slot["end"].isoformat(),
                                'timeZone': 'America/New_York',
                            },
                        }
                        
                        # Create the event in Google Calendar
                        created_event = service.events().insert(calendarId='primary', body=event).execute()
                        created_events.append(created_event)
            
            current_date += timedelta(days=1)
        
        return {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "created_events": created_events
        }
    
    except HttpError as error:
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))