from app.config import settings
from app.db.init_db import init_db
from app.routers.auth_routes import auth_router
from app.routers.product_routes import product_router
from app.routers.users import user_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI(root_path="/api/v1")
init_db()

origins = settings.ORIGINS
allowed_hosts = settings.ALLOWED_HOSTS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allomethods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(ProfilerMiddleware, profiling_enabled=True)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
app.add_middleware(GZipMiddleware, compresslevel=5)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
