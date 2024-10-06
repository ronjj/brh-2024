from fastapi import APIRouter, HTTPException
import requests
from typing import List, Dict, Any
# from datetime import datetime, date, timedelta
# from app.calendar_utils import get_calendar_service, get_free_busy
# from googleapiclient.errors import HttpError

router = APIRouter()

@router.get("/eateries")
async def get_eateries() -> List[Dict[str, Any]]:
    url = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"
    response = requests.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve data from Cornell Dining API")

    data = response.json()
    places = data["data"]["eateries"]
    eateries = []

    for eatery in places:
        name = eatery["nameshort"]
        about = eatery["aboutshort"]
        latitude = eatery["latitude"]
        longitude = eatery["longitude"]
        location = eatery["location"]
        eateryType = eatery["eateryTypes"][0]["descr"]

        dates = []
        for day in eatery["operatingHours"]:
            date = day["date"]
            events = []

            for event in day["events"]:
                descr = event["descr"]
                start = event["start"]
                end = event["end"]
                food = []

                for catType in event["menu"]:
                    # category = catType["category"]
                    for item in catType["items"]:
                        food.append(item["item"])

                events.append({
                    "Description": descr,
                    "Start": start,
                    "End": end,
                    "Food": food
                })

            dates.append({
                "Date": date,
                "Events": events
            })

        eateries.append({
            "Name": name,
            "About": about,
            "Latitude": latitude,
            "Longitude": longitude,
            "Location": location,
            "Type": eateryType,
            "Dates": dates
        })

    return eateries

# TODO: evaluate whether or not to add this AI-generated code
# @router.get("/suggest-meals")
# async def suggest_meals(date: date):
#     try:
#         service = get_calendar_service()
#         busy_slots = get_free_busy(service, date)
#         eateries = await get_eateries()
        
#         # Define meal times
#         meal_times = [
#             {"name": "Breakfast", "start": datetime.combine(date, datetime.min.time().replace(hour=7)), "duration": timedelta(minutes=30)},
#             {"name": "Lunch", "start": datetime.combine(date, datetime.min.time().replace(hour=12)), "duration": timedelta(minutes=45)},
#             {"name": "Dinner", "start": datetime.combine(date, datetime.min.time().replace(hour=18)), "duration": timedelta(minutes=60)}
#         ]
        
#         suggested_meals = []
        
#         for meal in meal_times:
#             # Find a free slot for the meal
#             meal_slot = find_free_slot(busy_slots, meal["start"], meal["duration"])
            
#             if meal_slot:
#                 # Find an open eatery for this meal time
#                 eatery = find_open_eatery(eateries, date, meal_slot["start"].time(), meal_slot["end"].time())
                
#                 if eatery:
#                     event_summary = f"{meal['name']} at {eatery['name']}"
                    
#                     event = {
#                         'summary': event_summary,
#                         'location': eatery['location'],
#                         'description': f"Suggested {meal['name']} at {eatery['name']}",
#                         'start': {
#                             'dateTime': meal_slot["start"].isoformat(),
#                             'timeZone': 'America/New_York',
#                         },
#                         'end': {
#                             'dateTime': meal_slot["end"].isoformat(),
#                             'timeZone': 'America/New_York',
#                         },
#                     }
                    
#                     created_event = service.events().insert(calendarId='primary', body=event).execute()
                    
#                     suggested_meals.append({
#                         "meal": meal['name'],
#                         "eatery": eatery['name'],
#                         "start": created_event["start"]["dateTime"],
#                         "end": created_event["end"]["dateTime"],
#                     })
        
#         return suggested_meals
#     except HttpError as error:
#         raise HTTPException(status_code=500, detail=str(error))

# def find_free_slot(busy_slots, start_time, duration):
#     end_time = start_time + duration
#     for slot in busy_slots:
#         slot_start = datetime.fromisoformat(slot['start'])
#         slot_end = datetime.fromisoformat(slot['end'])
#         if start_time >= slot_end or end_time <= slot_start:
#             continue
#         if start_time < slot_start:
#             end_time = min(end_time, slot_start)
#         else:
#             start_time = max(start_time, slot_end)
    
#     if end_time - start_time >= duration:
#         return {"start": start_time, "end": end_time}
#     return None

# def find_open_eatery(eateries, date, start_time, end_time):
#     day_name = date.strftime("%A")
#     for eatery in eateries:
#         for eatery_date in eatery['dates']:
#             if eatery_date['date'] == str(date):
#                 for event in eatery_date['events']:
#                     event_start = datetime.strptime(event['start'], "%H:%M").time()
#                     event_end = datetime.strptime(event['end'], "%H:%M").time()
#                     if event_start <= start_time and event_end >= end_time:
#                         return eatery
#     return None