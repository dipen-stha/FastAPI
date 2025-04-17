from typing import Annotated

from fastapi import Request, Response, Depends, status, HTTPException

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from sqlmodel import Session, select
from starlette.responses import JSONResponse

from app.services.auth import get_current_user, oauth2_scheme
from app.db.session import get_db
from app.db.models.user import User


class CustomAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # if "login" or "docs" in request.url.path.split("/"):
        if any(part in request.url.path.split("/") for part in ["login", "logout", "docs"]):
            response = await call_next(request)
            return response
        request.state.user = None
        db = next(get_db())
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Unauthorized"})
        token = auth_header.split(" ")[1]
        user = await get_current_user(token, db)
        if user:
            request.state.user = user
        response = await call_next(request)
        return response
