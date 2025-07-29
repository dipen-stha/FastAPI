from sqlalchemy.exc import NoResultFound
from sqlmodel import select

from app.db.models import RolePermissionLink
from app.db.models.user import Permission, Role
from app.db.session import get_db
from app.utils.enum.permissions import PERMISSIONS


def seed_role():
    permission_for_role = [
        PERMISSIONS.get("user_create").get("name"),
        PERMISSIONS.get("user_update").get("name"),
        PERMISSIONS.get("list_all_users").get("name"),
        PERMISSIONS.get("create_product").get("name"),
        PERMISSIONS.get("update_product").get("name"),
        PERMISSIONS.get("delete_product").get("name"),
        PERMISSIONS.get("list_all_product").get("name"),
        PERMISSIONS.get("create_category").get("name"),
        PERMISSIONS.get("update_category").get("name"),
        PERMISSIONS.get("delete_category").get("name"),
        PERMISSIONS.get("list_all_category").get("name"),
        PERMISSIONS.get("list_all_user_cart").get("name"),
    ]
    db = next(get_db())
    permissions = db.exec(
        select(Permission.id).where(Permission.name.in_(permission_for_role))
    )
    if not permissions:
        raise NoResultFound("No permissions found")

    role = Role(name="Admin User", display_name="Admin User")
    db.add(role)
    db.commit()
    db.refresh(role)
    role_permissions_link_instances = [
        RolePermissionLink(permission_id=permission_id, role_id=role.id)
        for permission_id in permissions
    ]
    db.add_all(role_permissions_link_instances)
    db.commit()

    return


if __name__ == "__main__":
    seed_role()
