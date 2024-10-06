from typing import List, Dict
import datetime
from app.calendar_utils import parse_time

GYM_SCHEDULE = {
    "Helen Newman": {
        "Monday": {"open": "06:00", "close": "21:00"},
        "Tuesday": {"open": "06:00", "close": "21:00"},
        "Wednesday": {"open": "06:00", "close": "21:00"},
        "Thursday": {"open": "06:00", "close": "21:00"},
        "Friday": {"open": "10:00", "close": "20:00"},
        "Saturday": {"open": "10:00", "close": "20:00"},
        "Sunday": {"open": "10:00", "close": "20:00"}
    },
    "Noyes": {
        "Monday": {"open": "07:00", "close": "23:00"},
        "Tuesday": {"open": "07:00", "close": "23:00"},
        "Wednesday": {"open": "07:00", "close": "23:00"},
        "Thursday": {"open": "07:00", "close": "23:00"},
        "Friday": {"open": "14:00", "close": "22:00"},
        "Saturday": {"open": "14:00", "close": "22:00"},
        "Sunday": {"open": "14:00", "close": "22:00"}
    },
    "Teagle Downstairs": {
        "Monday": [{"open": "07:00", "close": "08:30"}, {"open": "10:00", "close": "22:45"}],
        "Tuesday": [{"open": "07:00", "close": "08:30"}, {"open": "10:00", "close": "22:45"}],
        "Wednesday": [{"open": "07:00", "close": "08:30"}, {"open": "10:00", "close": "22:45"}],
        "Thursday": [{"open": "07:00", "close": "08:30"}, {"open": "10:00", "close": "22:45"}],
        "Friday": {"open": "07:00", "close": "22:45"},
        "Saturday": {"open": "12:00", "close": "17:30"},
        "Sunday": {"open": "12:00", "close": "17:30"}
    },
    "Teagle Upstairs": {
        "Monday": {"open": "07:00", "close": "22:45"},
        "Tuesday": {"open": "07:00", "close": "22:45"},
        "Wednesday": {"open": "07:00", "close": "22:45"},
        "Thursday": {"open": "07:00", "close": "22:45"},
        "Friday": {"open": "07:00", "close": "22:45"},
        "Saturday": {"open": "12:00", "close": "17:30"},
        "Sunday": {"open": "12:00", "close": "17:30"}
    },
    "Toni Morrison": {
        "Monday": {"open": "14:00", "close": "23:00"},
        "Tuesday": {"open": "14:00", "close": "23:00"},
        "Wednesday": {"open": "14:00", "close": "23:00"},
        "Thursday": {"open": "14:00", "close": "23:00"},
        "Friday": {"open": "12:00", "close": "22:00"},
        "Saturday": {"open": "12:00", "close": "22:00"},
        "Sunday": {"open": "12:00", "close": "22:00"}
    }
}

def get_gym_hours(gym: str, day: str) -> List[Dict[str, datetime.time]]:
    schedule = GYM_SCHEDULE[gym][day]
    if isinstance(schedule, list):
        return [{"open": parse_time(slot["open"]), "close": parse_time(slot["close"])} for slot in schedule]
    else:
        return [{"open": parse_time(schedule["open"]), "close": parse_time(schedule["close"])}]

def get_gym_availability(gym: str, date: datetime.date, free_slots: List[Dict]):
    day_name = date.strftime("%A")
    gym_hours = get_gym_hours(gym, day_name)
    
    available_slots = [] # times when you are free and the gym is open
    
    # Calculate available slots based on gym hours and free slots
    for hours in gym_hours:
        current_time = hours["open"]
        for free in sorted(free_slots, key=lambda x: x["start"]):
            free_start = free["start"]
            free_end = free["end"]
            
            # Check if the free slot overlaps with gym hours
            if current_time < free_start and free_start < hours["close"]:
                available_slots.append({"start": current_time, "end": free_start})
            current_time = max(current_time, free_end)
        
        if current_time < hours["close"]:
            available_slots.append({"start": current_time, "end": hours["close"]})
    
    return available_slots