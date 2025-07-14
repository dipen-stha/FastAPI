from typing import Annotated

from sqlmodel import select, Session
from starlette.responses import JSONResponse

from app.db import crud
from app.db.crud import assign_role, create_user_profile, update_user_profile
from app.db.models.user import Role, User
from app.db.session import get_db
from app.schemas.user import (
    PermissionIn,
    ProfileIn,
    ProfileInPatch,
    ProfileOut,
    RoleIn,
    RoleOut,
    UserDetailSchema,
    UserOut,
    UserRoleLinkSchema,
    UserRoleSchema,
)
from app.services.auth import get_current_user

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError


user_router = APIRouter(
    prefix="/users",
)


@user_router.get("/list/")
async def list_users(db: Annotated[Session, Depends(get_db)]) -> list[UserOut]:
    users = crud.get_users(db=db)
    return users


@user_router.post("/permissions/create/")
async def create_permission(
    permission: PermissionIn, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    try:
        permission = await crud.create_permission(db=db, permission=permission)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Permission created", "data": permission.model_dump()},
        )
    except HTTPException as err:
        return JSONResponse(status_code=err.status_code, content={"error": err.detail})


@user_router.post("/roles/create/")
async def create_roles(
    role: RoleIn, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    try:
        role = await crud.create_role(db=db, role=role)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Role created", "data": role.model_dump()},
        )
    except HTTPException as err:
        return JSONResponse(status_code=err.status_code, content={"error": err.detail})


@user_router.get("/roles/get/", response_model=list[RoleOut])
def fetch_roles(db: Annotated[Session, Depends(get_db)]):
    query = select(Role)
    roles = db.exec(query).all()
    return roles


@user_router.post("/assign-role/")
async def assign_roles(
    user_role: UserRoleLinkSchema, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    assign_role(user_role, db)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="Role assigned to the user"
    )


@user_router.get("/user-roles/{user_id}/", response_model=UserRoleSchema)
def user_roles(
    user_id: int, db: Annotated[Session, Depends(get_db)]
) -> UserRoleSchema | JSONResponse:
    try:
        user = db.exec(select(User).where(User.id == user_id)).first()
        return user
    except ResponseValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Validation Error - {e}"},
        )
    except Exception as err:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"There was an error - {err}"},
        )


@user_router.get("/self/me/")
async def get_self(
    request: Request, current_user: Annotated[User, Depends(get_current_user)]
) -> JSONResponse:
    user_details = UserDetailSchema.from_orm(current_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={**user_details.model_dump()}
    )


@user_router.post("/profile/create/")
async def create_profile(
    profile: ProfileIn, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    user_profile = await create_user_profile(profile, db)
    user_profile_data = ProfileOut.model_validate(user_profile)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"data": jsonable_encoder(user_profile_data.model_dump())},
    )


@user_router.patch("/profile/update/{profile_id}/")
async def update_profile(
    profile_id: int, profile: ProfileInPatch, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    updated_instance = await update_user_profile(profile_id, profile, db)
    updated_profile_data = ProfileOut.model_validate(updated_instance)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": jsonable_encoder(updated_profile_data.model_dump())},
    )
