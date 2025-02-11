from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, status

from sqlmodel import Session
from starlette.responses import JSONResponse

from app.db import crud
from app.db.session import get_db
from app.schemas.user import UserOut
from app.db.models.user import User, Role
from app.utils.mixins import CustomResponse

user_router = APIRouter(
    prefix="/users",
)

@user_router.get('/list/')
async def list_users(db:Annotated[Session, Depends(get_db)]) -> list[UserOut]:
    users = crud.get_users(db=db)
    return users

@user_router.post('/roles/create/')
async def create_roles(role: Role, db:Annotated[Session, Depends(get_db)]):
    role = Role(name=role.name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
        "message": "Role created",
        "data": role.model_dump()
    })