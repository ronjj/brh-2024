from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Calendar Integration API"
    GOOGLE_CALENDAR_CREDENTIALS: str = "credentials.json"

    class Config:
        env_file = ".env"

settings = Settings()