from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserResponse
from app.security import verify_password
from jose import JWTError, jwt
import shutil
import uuid
import os

router= APIRouter(prefix="/users", tags=["Users"])

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=[os.getenv("JWT_ALGORITHM")])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
        )
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/me/profile-pic")
def upload_profile_pic(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
                status_code=400,
                detail="Invalid file type, Only JPEG, PNG, GIF and WebP, allowed"
            )
    MAX_SIZE = 5 * 1024 * 1024
    contents = file.file.read()
    if len(contents) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    os.makedirs("uploads/profiles", exist_ok=True)
    file_path = f"uploads/profiles/{filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    current_user.profile_pic_url = f"/static/profiles/{filename}"
    db.commit()
    db.refresh(current_user)

    return current_user
            

