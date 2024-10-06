from fastapi import FastAPI
from app.api import calendar, dining, gym
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
app.include_router(dining.router, prefix="/dining", tags=["dining"])
app.include_router(gym.router, prefix="/gym", tags=["gym"])

@app.get("/")
async def root():
    return {"message": "Omnisplit"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
