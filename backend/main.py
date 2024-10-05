from fastapi import FastAPI
from app.api.router import router
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Let's get swole"}