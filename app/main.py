from fastapi import FastAPI

from app.db.init_db import init_db
from app.routers.auth_routes import auth_router
from app.routers.product_routes import product_router
from app.routers.users import user_router
from app.services.middlewares import CustomAuthenticationMiddleware

app = FastAPI()

init_db()

app.add_middleware(
    CustomAuthenticationMiddleware
)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)

