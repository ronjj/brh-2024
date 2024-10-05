from fastapi import FastAPI
from api.router import router  # Changed from app.api.router
from config import settings  # Changed from app.config

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Let's get swole"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)