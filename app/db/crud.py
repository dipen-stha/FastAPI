from fastapi import Depends, HTTPException, status
from slugify import slugify

from sqlmodel import Session, select, delete
from starlette.responses import JSONResponse

from app.db.models.user import User, Role, Permission, RolePermissionLink, UserRoleLink
from app.schemas.user import UserIn, UserOut, RoleIn, PermissionIn, UserRoleLinkSchema
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

async def create_permission(permission: PermissionIn, db:Session = Depends(get_db)) -> Permission:
    data = permission.model_dump()
    data['name'] = slugify(data.get('display_name'))
    permission_instance = Permission(**data)
    db.add(permission_instance)
    db.commit()
    return permission_instance

async def set_role_permissions(role_id: int, permission_ids: list[int], db:Session = Depends(get_db)):
    statement = delete(RolePermissionLink).where(RolePermissionLink.role_id == role_id)
    db.exec(statement)
    db.flush()

    new_link_instances = [RolePermissionLink(role_id=role_id, permission_id=perm_id) for perm_id in permission_ids]
    db.add_all(new_link_instances)

async def create_role(role: RoleIn, db:Session = Depends(get_db)) -> Role:
    try:
        with db.begin():
            role_data = role.model_dump()
            permissions = role_data.pop('permissions')
            role_instance = Role(**role_data)
            db.add(role_instance)
            db.flush()
            db.refresh(role_instance)
            await set_role_permissions(role_instance.id, permissions, db)
            return role_instance

    except Exception as e:
        db.rollback()
        raise e


def assign_role(user_role: UserRoleLinkSchema, db:Session):
    try:
        with db.begin():
            statement = delete(RolePermissionLink).where(RolePermissionLink.role_id == user_role.user_id)
            db.exec(statement)

            user_roles = [UserRoleLink(user_id=user_role.user_id, role_id=role_id) for role_id in user_role.role_ids]
            db.add_all(user_roles)
    except Exception as e:
        db.rollback()
