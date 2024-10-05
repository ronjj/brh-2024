from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import settings

def get_calendar_service(token):
    creds = Credentials.from_authorized_user_file(settings.GOOGLE_CALENDAR_CREDENTIALS, ['https://www.googleapis.com/auth/calendar'])
    return build('calendar', 'v3', credentials=creds)