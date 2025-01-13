from typing import Annotated

from fastapi import APIRouter, Form, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlmodel import Session

from app.db import crud
from app.db.session import get_db
from app.db.models.user import Role

from app.schemas.user import UserLogin, UserIn, UserOut

auth_router = APIRouter(
    prefix='/user'
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post('/login')
def login(username: str = Form(), password: str = Form()):
    if not username or not password:
        return Response({
            "message": "Username or password missing"
        })
    return {
        "message": "Logged in successfully"
        }

@auth_router.post('/create/', response_model=list[UserOut])
async def create_user(user: UserIn, db:Session = Depends(get_db)):
    return crud.create_user(db, user=user)

@auth_router.get('/list/')
async def list_users(db:Session = Depends(get_db)) -> list[UserOut]:
    users = crud.get_users(db=db)
    return users

@auth_router.post('/roles/create/')
async def create_roles(name: str, db:Session = Depends(get_db)):
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return Response({"message": f"Successfully created new role - {role.name}"})