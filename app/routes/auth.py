from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.security import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user_data.email).first()
    if user_exist:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
                )

    hashed = hash_password(user_data.password)
    new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed
            )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=Token)
def login(
        email: str,
        password: str,
        db: Session = Depends(get_db)
        ):

        user = db.query(User).filter(User.email == email).first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Login Error"
                    )

        access_token = create_access_token(
                data={"sub": str(user.id)},
                expires_delta=timedelta(minutes=60)
                )

        return Token(access_token=access_token)
