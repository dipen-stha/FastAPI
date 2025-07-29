from typing import Annotated

from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import selectinload
from sqlmodel import func, select, Session
from starlette.responses import JSONResponse

from app.db import crud
from app.db.crud import (
    assign_role,
    create_user_cart,
    create_user_profile,
    update_user_cart,
    update_user_profile,
)
from app.db.models import Product
from app.db.models.user import Role, User, UserCart
from app.db.session import get_db
from app.schemas.user import (
    PermissionIn,
    ProfileIn,
    ProfileInPatch,
    ProfileOut,
    RoleIn,
    RoleOut,
    UserCartIn,
    UserCartOut,
    UserDetailSchema,
    UserOut,
    UserRoleLinkSchema,
    UserRoleSchema,
)
from app.schemas.filters import BaseFilter
from app.services.auth import get_current_user

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
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
    except IntegrityError:
        return JSONResponse(
            content={"message": "Permission with this name already exists"},
            status_code=status.HTTP_409_CONFLICT,
        )


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
    try:
        _, errors = assign_role(user_role, db)
        if errors:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"errors": errors}
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content="Role assigned to the user"
        )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "User with given ID found"},
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


@user_router.post("/cart/create/")
def user_cart_create(
    user_cart: UserCartIn, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    user_cart_instance = create_user_cart(user_cart, db)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"data": user_cart_instance.model_dump()},
    )


@user_router.patch("/cart/update/{user_cart_id}/")
def user_cart_update(
    user_cart_id: int, user_cart: UserCartIn, db: Annotated[Session, Depends(get_db)]
) -> JSONResponse:
    try:
        updated_user_cart_data = update_user_cart(user_cart_id, user_cart, db)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": updated_user_cart_data.model_dump()},
        )
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "User with given ID found"},
        )


@user_router.get("/cart/get/all/")
def fetch_all_user_carts(
    db: Annotated[Session, Depends(get_db)],
    filter_query: Annotated[BaseFilter, Query()],
) -> JSONResponse:
    try:
        user_carts = db.exec(
            select(UserCart)
            .options(selectinload(UserCart.product), selectinload(UserCart.user))
            .offset(filter_query.offset)
            .limit(filter_query.limit)
        ).all()
        user_carts_data = [
            UserCartOut.model_validate(user_cart).model_dump()
            for user_cart in user_carts
        ]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": user_carts_data},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"There was an error - {e}"},
        )


@user_router.get("/cart/get/self/")
def fetch_self_product_cart(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    try:
        user_carts = db.exec(
            select(UserCart)
            .options(selectinload(UserCart.product), selectinload(UserCart.user))
            .where(UserCart.user_id == current_user.id)
        ).all()
        total_price = db.exec(
            select(func.sum(UserCart.quantity * Product.price))
            .where(UserCart.user_id == current_user.id)
            .join(Product)
        ).one()
        user_carts_data = [
            UserCartOut.model_validate(user_cart).model_dump()
            for user_cart in user_carts
        ]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "data": {"user_cart": user_carts_data, "total_price": total_price or 0}
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"There was an error - {e}"},
        )
