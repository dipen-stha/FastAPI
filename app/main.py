from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.init_db import init_db
from app.routers.auth_routes import auth_router
from app.routers.product_routes import product_router
from app.routers.users import user_router
from app.services.middlewares import CustomAuthenticationMiddleware, ProfilerMiddleware

app = FastAPI()

init_db()

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CustomAuthenticationMiddleware,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(ProfilerMiddleware, profiling_enabled=True)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)

