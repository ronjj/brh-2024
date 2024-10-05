import firebase_admin
from firebase_admin import credentials
from app.config import settings

def get_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
        firebase_admin.initialize_app(cred)
    return firebase_admin.get_app()