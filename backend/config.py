from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Calendar Integration API"
    FIREBASE_CREDENTIALS: str
    GOOGLE_CALENDAR_CREDENTIALS: str

    class Config:
        env_file = ".env"

settings = Settings()