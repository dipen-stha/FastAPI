from fastapi import Depends, HTTPException
from pydantic import ValidationError

from sqlmodel import Session, select

from app.db.models.user import User
from app.schemas.user import UserIn, UserOut
from app.db.session import get_db
from app.services.auth import get_password_hash

def validate_username(db: Session, username: str):
    query = select(User).where(User.username == username)
    existing_user = db.exec(query).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = db.exec(statement).one()
    return user

def create_user(db:Session, user:UserIn):
    validate_username(db, user.username)
    data = user.model_dump(exclude={"id"})
    password =  data.pop('hashed_password')
    data['hashed_password'] = get_password_hash(password)
    user_data = User(**data)
    db.add(user_data)
    db.commit()
    return user

def get_users( user_id: int | None = None, db:Session = Depends(get_db)) -> UserOut | list[UserOut] | None:
    if user_id:
        return db.get(User, user_id)
    else:
        statement = select(User).where(User.is_active == True)
        results = db.exec(statement).all()
        return results