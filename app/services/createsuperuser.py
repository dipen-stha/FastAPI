from app.db.models import User
from app.db.session import get_db
from app.utils.validators import validate_email

def create_superuser():
    name = input("Enter name: ")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    repeat_password = input("Repeat password: ")

    if not password == repeat_password:
        print("Passwords do not match")
        return
    if not validate_email(email):
        print("Enter a valid email")
        return

    from app.utils.helpers import get_password_hash
    hashed_password = get_password_hash(password)
    user = User(name=name, username=username, email=email, hashed_password=hashed_password, is_superuser=True)
    session = next(get_db())
    session.add(user)
    session.commit()
    session.refresh(user)

    print(f"Superuser created with username: {user.username}")


if __name__ == "__main__":
    create_superuser()

