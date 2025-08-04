from datetime import timedelta
from typing import Annotated

from sqlmodel import Session

from app.db import crud
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.user import Token, UserIn, UserLogin, UserOut
from app.services import auth

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse


auth_router = APIRouter(prefix="/auth")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@auth_router.post("/create/", tags=["User"])
def create_user(user: UserIn, db: Annotated[Session, Depends(get_db)]):
    user = crud.create_user(db, user=user)
    if user:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User created", "data": user.dict()},
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content="Failed to create user"
        )


@auth_router.get("/user/me/", response_model=UserOut, tags=["User"])
def get_users_me(current_user: Annotated[User, Depends(auth.get_current_active_user)]):
    if current_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return UserOut(**current_user.model_dump())


@auth_router.post("/login/token/", response_model=Token, tags=["Authentication"])
def login(user_login: UserLogin, db: Annotated[Session, Depends(get_db)]):
    try:
        user = auth.authenticate_user(user_login, db)
        if not user.is_active or user.is_archived:
            raise HTTPException(status_code=400, detail="Inactive user")
        return Token(
            access_token=auth.create_access_token(
                data={"user_id": user.id, "username": user.username},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            )
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
