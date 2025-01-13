from fastapi import Depends

from sqlmodel import Session, select

from app.db.models.user import User
from app.schemas.user import UserIn, UserOut
from app.db.session import get_db


def create_user(db:Session, user:UserIn):
    user = User(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users( user_id: int | None = None, db:Session = Depends(get_db)) -> UserOut | list[UserOut] | None:
    if user_id:
        return db.get(User, user_id)
    else:
        statement = select(User).where(User.is_active == True)
        results = db.exec(statement).all()
        return results