from fastapi import Depends, HTTPException, status
from firebase_admin import auth
from app.firebase_utils import get_firebase_app

def get_current_user(token: str = Depends(auth.verify_id_token)):
    try:
        decoded_token = auth.verify_id_token(token, app=get_firebase_app())
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
