import datetime
import os.path
from typing import List, Dict

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Gym schedule representation
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

def get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CALENDAR_CREDENTIALS, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    return build("calendar", "v3", credentials=creds)

def get_upcoming_events(service, max_results=10):
    now = datetime.datetime.utcnow().isoformat() + "Z"
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return events_result.get("items", [])

def parse_time(time_str: str) -> datetime.time:
    return datetime.datetime.strptime(time_str, "%H:%M").time()

def get_gym_hours(gym: str, day: str) -> List[Dict[str, datetime.time]]:
    schedule = GYM_SCHEDULE[gym][day]
    if isinstance(schedule, list):
        return [{"open": parse_time(slot["open"]), "close": parse_time(slot["close"])} for slot in schedule]
    else:
        return [{"open": parse_time(schedule["open"]), "close": parse_time(schedule["close"])}]

def find_available_slots(gym: str, date: datetime.date, events: List[Dict]):
    day_name = date.strftime("%A")
    gym_hours = get_gym_hours(gym, day_name)
    
    # Convert events to datetime objects
    calendar_events = []
    for event in events:
        start = datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
        end = datetime.datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
        if start.date() == date:
            calendar_events.append({"start": start.time(), "end": end.time()})
    
    available_slots = []
    for hours in gym_hours:
        current_time = hours["open"]
        for event in sorted(calendar_events, key=lambda x: x["start"]):
            if current_time < event["start"] and event["start"] < hours["close"]:
                available_slots.append({"start": current_time, "end": event["start"]})
            current_time = max(current_time, event["end"])
        
        if current_time < hours["close"]:
            available_slots.append({"start": current_time, "end": hours["close"]})
    
    return available_slots