from slugify import slugify
from sqlalchemy.exc import NoResultFound
from sqlmodel import delete, select, Session

from app.db.models.user import (
    Permission,
    Profile,
    Role,
    RolePermissionLink,
    User,
    UserCart,
    UserRoleLink,
)
from app.schemas.user import (
    PermissionIn,
    PermissionOut,
    ProfileIn,
    ProfileInPatch,
    ProfileOut,
    RoleIn,
    RoleOut,
    UserCartIn,
    UserCartOut,
    UserIn,
    UserOut,
    UserRoleLinkSchema,
)
from app.utils.helpers import get_password_hash
from app.utils.model_utilty import update_model_instance

from fastapi import HTTPException


def validate_username(db: Session, username: str):
    query = select(User).where(User.username == username)
    existing_user = db.exec(query).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")


def get_user_by_username(db: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    user = db.exec(statement).one()
    return user


def create_user(db: Session, user: UserIn):
    validate_username(db, user.username)
    data = user.model_dump(exclude={"id"})
    password = data.pop("hashed_password")
    data["hashed_password"] = get_password_hash(password)
    user_data = User(**data)
    db.add(user_data)
    db.commit()
    return user


def get_users(
    db: Session, user_id: int | None = None
) -> UserOut | list[UserOut] | None:
    if user_id:
        return db.get(User, user_id)
    else:
        statement = select(User).where(User.is_active)
        results = db.exec(statement).all()
        return results


async def create_permission(permission: PermissionIn, db: Session) -> PermissionOut:
    data = permission.model_dump()
    data["name"] = slugify(data.get("display_name"))
    permission_instance = Permission(**data)
    db.add(permission_instance)
    db.commit()
    permission = PermissionOut.model_validate(permission_instance)
    return permission


async def set_role_permissions(role_id: int, permission_ids: list[int], db: Session):
    statement = delete(RolePermissionLink).where(RolePermissionLink.role_id == role_id)
    db.exec(statement)
    db.flush()

    new_link_instances = [
        RolePermissionLink(role_id=role_id, permission_id=perm_id)
        for perm_id in permission_ids
    ]
    db.add_all(new_link_instances)


async def create_role(role: RoleIn, db: Session) -> RoleOut:
    try:
        with db.begin():
            role_data = role.model_dump()
            permissions = role_data.pop("permissions")
            role_instance = Role(**role_data)
            db.add(role_instance)
            db.flush()
            db.refresh(role_instance)
            await set_role_permissions(role_instance.id, permissions, db)
            role = RoleOut.model_validate(role_instance)
            return role

    except Exception as e:
        db.rollback()
        raise e


def assign_role(user_role: UserRoleLinkSchema, db: Session) -> (list, dict):
    errors = {}
    user_roles = []
    try:
        user = db.exec(select(User).where(User.id == user_role.user_id)).first()
        existing_roles = set(db.exec(select(Role.id)).all())
        roles = set(user_role.role_ids)
        non_existing = roles - existing_roles
        if not user:
            errors["users"] = f"User with pk {user_role.user_id} not found" f""
        if non_existing:
            errors["roles"] = f"Roles with pks {list(non_existing)} Not Found"
        with db.begin():
            statement = delete(RolePermissionLink).where(
                RolePermissionLink.role_id == user_role.user_id
            )
            db.exec(statement)

            user_roles = [
                UserRoleLink(user_id=user.id, role_id=role_id)
                for role_id in user_role.role_ids
            ]
            db.add_all(user_roles)
            db.commit()
    except Exception:
        db.rollback()
    return user_roles, errors


async def create_user_profile(
    user_profile: ProfileIn, db: Session
) -> ProfileOut | None:
    try:
        user_profile_data = user_profile.model_dump()
        user_id = user_profile_data.pop("user")
        user_profile_data["user_id"] = user_id
        profile_query = select(Profile).where(Profile.user_id == user_id)
        existing_user_profile = db.exec(profile_query).first()
        if existing_user_profile:
            raise HTTPException(
                status_code=500, detail="Profile for this already exists"
            )
        user_profile_instance = Profile(**user_profile_data)
        db.add(user_profile_instance)
        db.commit()
        db.refresh(user_profile_instance)
        return user_profile_instance
    except Exception as e:
        raise e


async def fetch_user_profile(db: Session, profile_id: int) -> Profile | None:
    profile_instance = db.exec(select(Profile).where(Profile.id == profile_id)).first()
    return profile_instance


async def update_user_profile(
    profile_id: int, data: ProfileInPatch, db: Session
) -> Profile | None:
    user_profile_instance = await fetch_user_profile(db, profile_id)
    if not user_profile_instance:
        raise HTTPException(status_code=404, detail="User not found")
    updated_profile_instance = update_model_instance(
        data.model_dump(exclude_unset=True), user_profile_instance
    )
    db.add(updated_profile_instance)
    db.commit()
    db.refresh(updated_profile_instance)
    return updated_profile_instance


def create_user_cart(user_cart: UserCartIn, db: Session) -> UserCartOut:
    user_cart_instance = UserCart(**user_cart.model_dump())
    db.add(user_cart_instance)
    db.commit()
    db.refresh(user_cart_instance)
    user_cart = UserCartOut.model_validate(user_cart_instance)
    return user_cart


def update_user_cart(
    user_cart_id: int, user_cart: UserCartIn, db: Session
) -> UserCartOut:
    user_cart_instance: UserCart = db.exec(
        select(UserCart).where(UserCart.user_id == user_cart_id)
    ).first()
    if not user_cart_instance:
        raise NoResultFound
    updated_instance = update_model_instance(user_cart, user_cart_instance)
    db.add(updated_instance)
    db.commit()
    updated_user_cart = UserCartOut.model_validate(updated_instance)
    return updated_user_cart
