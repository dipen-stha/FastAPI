from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, status

from sqlmodel import Session
from starlette.responses import JSONResponse

from app.db import crud
from app.db.session import get_db
from app.schemas.user import UserOut, RoleIn, PermissionIn
from app.db.models.user import User, Role
from app.utils.mixins import CustomResponse

user_router = APIRouter(
    prefix="/users",
)

@user_router.get('/list/')
async def list_users(db:Annotated[Session, Depends(get_db)]) -> list[UserOut]:
    users = crud.get_users(db=db)
    return users


@user_router.post('/permissions/create/')
async def create_permission(permission: PermissionIn, db: Session = Depends(get_db)) -> JSONResponse:
    try:
        permission = crud.create_permission(db=db, permission=permission)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            'message': 'Permission created',
            'data': permission.model_dump()
        })
    except HTTPException as err:
        return JSONResponse(status_code=err.status_code, content={"error": err.detail})


@user_router.post('/roles/create/')
async def create_roles(role: RoleIn, db:Annotated[Session, Depends(get_db)]) -> JSONResponse:
    try:
        role = crud.create_role(db=db, role=role)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
            "message": "Role created",
            "data": role.model_dump()
        })
    except HTTPException as err:
        return JSONResponse(status_code=err.status_code, content={"error": err.detail})