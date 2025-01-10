from typing import Annotated

from fastapi import APIRouter, Form, Response
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserLogin, UserIn

auth_router = APIRouter(
    prefix='/user'
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post('/login')
def login(username: str = Form(), password: str = Form()):
    if not username or not password:
        return Response({
            "message": "Username or password missing"
        })
    return {
        "message": "Logged in successfully"
        }

@auth_router.post('/create')
async def create_user(user: UserIn):
    return {"user": "user"}

@auth_router.get('/list')
async def list_users():
    return {"Users": "users"}