from fastapi import FastAPI
from app.api import calendar
from app.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(calendar.router, prefix="/calendar", tags=["calendar"])

@app.get("/")
async def root():
    return {"message": "Omnisplit"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
