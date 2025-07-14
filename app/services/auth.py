from datetime import datetime, timedelta, UTC
from typing import Annotated

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Session

from app.config import settings
from app.db import crud
from app.db.models import User
from app.db.session import get_db
from app.schemas.user import TokenData, UserLogin
from app.utils.helpers import verify_password

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http:localhost:8080/auth/token")

# Password hashing utility


def authenticate_user(user_login: UserLogin, db: Session) -> User | None:
    user = crud.get_user_by_username(db, user_login.username)
    if not user or not verify_password(user_login.password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)] = Session,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


CURRENT_USER = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(current_user: CURRENT_USER) -> User:
    if not current_user:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
