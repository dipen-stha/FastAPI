from typing import Annotated

from fastapi import Depends, status, HTTPException

from app.services import auth
from app.db.models import User

class PermissionChecker:
    def __init__(self, required_permissions: list[str]):
        self.required_permissions = required_permissions

    def __call__(self, user: Annotated[User, Depends(auth.get_current_user)]):
        if not user.is_superuser:
            user_permission = set()
            for role in user.roles:
                user_permission.update([p.name for p in role.permissions])

            if not any(perm in user_permission for perm in self.required_permissions):
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