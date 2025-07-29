from sqlmodel import select

from app.db.models import Permission
from app.db.session import get_db
from app.utils.enum.permissions import PERMISSIONS


def sync_permission():
    permissions = PERMISSIONS
    permission_names = [item.get("name") for item in permissions.values()]
    db = next(get_db())
    existing_permission = set(db.exec(select(Permission.name)).all())
    to_create_permissions = set(permission_names) - existing_permission
    to_create_permission_objects = [
        item
        for item in permissions.values()
        if item.get("name") in to_create_permissions
    ]
    to_create_permission_instances = [
        Permission(name=item.get("name"), display_name=item.get("display_name"))
        for item in to_create_permission_objects
    ]
    if to_create_permission_instances:
        db.add_all(to_create_permission_instances)
        db.flush()
        db.commit()

    return


if __name__ == "__main__":
    sync_permission()
