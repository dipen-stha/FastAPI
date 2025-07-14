from typing import Annotated

from app.db.models import User
from app.services import auth

from fastapi import Depends, HTTPException, status


def get_required_permissions(permissions: list[str]):
    return PermissionChecker(required_permissions=permissions)


class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = set(required_permissions)

    def __call__(self, user: Annotated[User, Depends(auth.get_current_user)]):
        if not user.is_superuser:
            user_permission = set()
            for role in user.roles:
                user_permission.update([p.name for p in role.permissions])

            if not self.required_permissions.intersection(user_permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this action",
                )
        return user


class RoleChecker:
    def __init__(self, required_roles: str | list[str]):
        self.required_roles = required_roles

    def __call__(self, user: Annotated[User, Depends(auth.get_current_user)]):
        if not user.is_superuser:
            if not any(role in user.roles for role in self.required_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to perform this action",
                )
        return user


super_role_required = RoleChecker(required_roles=["admin"])
