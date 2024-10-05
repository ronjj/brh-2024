import datetime
import os.path
from typing import List, Dict
from zoneinfo import ZoneInfo

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

EST_TIMEZONE = ZoneInfo("America/New_York")

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

# not needed for now
# def get_upcoming_events(service, max_results=10):
#     now = datetime.datetime.utcnow().isoformat() + "Z"
#     events_result = service.events().list(
#         calendarId="primary",
#         timeMin=now,
#         maxResults=max_results,
#         singleEvents=True,
#         orderBy="startTime",
#     ).execute()
#     return events_result.get("items", [])

# not needed for now
# def get_events_for_date(service, date: datetime.date):
#     start_datetime = datetime.datetime.combine(date, datetime.time.min).astimezone(datetime.timezone.utc)
#     end_datetime = datetime.datetime.combine(date, datetime.time.max).astimezone(datetime.timezone.utc)
    
#     start_str = start_datetime.isoformat()
#     end_str = end_datetime.isoformat()

#     events_result = service.events().list(
#         calendarId="primary",
#         timeMin=start_str,
#         timeMax=end_str,
#         singleEvents=True,
#         orderBy="startTime",
#     ).execute()
#     return events_result.get("items", [])

def get_free_busy(service, date: datetime.date):
    # Convert the date to EST timezone
    start_datetime = datetime.datetime.combine(date, datetime.time.min).replace(tzinfo=EST_TIMEZONE)
    end_datetime = datetime.datetime.combine(date, datetime.time.max).replace(tzinfo=EST_TIMEZONE)
    
    body = {
        "timeMin": start_datetime.isoformat(),
        "timeMax": end_datetime.isoformat(),
        "items": [{"id": "primary"}]  # You can add more calendar IDs here if needed
    }
    
    events_result = service.freebusy().query(body=body).execute()
    busy_slots = events_result["calendars"]["primary"]["busy"]
    
    return busy_slots

def parse_time(time_str: str) -> datetime.time:
    return datetime.datetime.strptime(time_str, "%H:%M").time()

def get_gym_hours(gym: str, day: str) -> List[Dict[str, datetime.time]]:
    schedule = GYM_SCHEDULE[gym][day]
    if isinstance(schedule, list):
        return [{"open": parse_time(slot["open"]), "close": parse_time(slot["close"])} for slot in schedule]
    else:
        return [{"open": parse_time(schedule["open"]), "close": parse_time(schedule["close"])}]

# returns a list of available slots for the gym on the given date, in the format of a list of dictionaries with start and end times
def find_available_slots(gym: str, date: datetime.date, busy_slots: List[Dict]):
    day_name = date.strftime("%A")
    gym_hours = get_gym_hours(gym, day_name)
    
    # Convert busy slots to datetime.time objects in EST
    busy_times = []
    for slot in busy_slots:
        start = datetime.datetime.fromisoformat(slot['start']).astimezone(EST_TIMEZONE).time()
        end = datetime.datetime.fromisoformat(slot['end']).astimezone(EST_TIMEZONE).time()
        busy_times.append({"start": start, "end": end})

    print(busy_times)
    
    available_slots = []
    for hours in gym_hours:
        current_time = hours["open"]
        for busy in sorted(busy_times, key=lambda x: x["start"]):
            if current_time < busy["start"] and busy["start"] < hours["close"]:
                available_slots.append({"start": current_time, "end": busy["start"]})
            current_time = max(current_time, busy["end"])
        
        if current_time < hours["close"]:
            available_slots.append({"start": current_time, "end": hours["close"]})
    
    return available_slots