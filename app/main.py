from fastapi import FastAPI

from app.db.init_db import init_db
from app.routers.auth_routes import auth_router
from app.routers.product_routes import order_router

app = FastAPI()

init_db()

app.include_router(auth_router)
app.include_router(order_router)

