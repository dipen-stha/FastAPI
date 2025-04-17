from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException, status, Request
from fastapi.exceptions import ResponseValidationError

from sqlmodel import Session, select
from starlette.responses import JSONResponse

from app.db import crud
from app.db.crud import assign_role
from app.db.session import get_db
from app.schemas.user import UserOut, RoleIn, PermissionIn, UserRoleLinkSchema, UserDetailSchema, UserRoleSchema, \
    RoleOut
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
        permission = await crud.create_permission(db=db, permission=permission)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            'message': 'Permission created',
            'data': permission.model_dump()
        })
    except HTTPException as err:
        return JSONResponse(status_code=err.status_code, content={"error": err.detail})


@user_router.post('/roles/create/')
async def create_roles(role: RoleIn, db:Annotated[Session, Depends(get_db)]) -> JSONResponse:
    try:
        role = await crud.create_role(db=db, role=role)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
            "message": "Role created",
            "data": role.model_dump()
        })
    except HTTPException as err:
        return JSONResponse(status_code=err.status_code, content={"error": err.detail})


@user_router.get('/roles/get/', response_model=list[RoleOut])
def fetch_roles(db: Session = Depends(get_db)):
    query = select(Role)
    roles = db.exec(query).all()
    return roles

@user_router.post('/assign-role/')
async def assign_roles(user_role: UserRoleLinkSchema, db: Session = Depends(get_db)) -> JSONResponse:
    assign_role(user_role, db)
    return JSONResponse(status_code=status.HTTP_200_OK, content="Role assigned to the user")

@user_router.get('/user-roles/{user_id}/', response_model=UserRoleSchema)
def user_roles(user_id: int, db: Annotated[Session, Depends(get_db)]) -> UserRoleSchema | JSONResponse:
    try:
        user = db.exec(select(User).where(User.id == user_id)).first()
        return user
    except ResponseValidationError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": f"Validation Error - {e}"})
    except Exception as err:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": f"There was an error - {err}"})


@user_router.get('/self/me/')
async def get_self(request: Request, db:Annotated[Session, Depends(get_db)]) -> JSONResponse:
    user = request.state.user
    user_details = UserDetailSchema.from_orm(user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={**user_details.model_dump()})