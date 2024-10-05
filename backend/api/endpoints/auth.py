from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/login")
async def login():
    # Implement Firebase authentication logic
    pass

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return current_user