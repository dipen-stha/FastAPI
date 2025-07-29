from collections.abc import Callable

from pyinstrument import Profiler
from pyinstrument.renderers import HTMLRenderer, SpeedscopeRenderer
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from app.db.session import get_db
from app.services.auth import get_current_user

from fastapi import FastAPI, HTTPException, Request, Response, status


class CustomAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # if "login" or "docs" in request.url.path.split("/"):
        try:
            if any(
                part in request.url.path.split("/")
                for part in ["login", "logout", "docs", "openapi.json", "debug_toolbar"]
            ):
                response = await call_next(request)
                return response
            request.state.user = None
            db = next(get_db())
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Unauthorized"},
                )
            token = auth_header.split(" ")[1]
            user = await get_current_user(token, db)
            if user:
                request.state.user = user
            response = await call_next(request)
            return response
        except HTTPException as exc:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content={"message": str(exc)}
            )
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"message": str(exc)},
            )


class ProfilerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, profiling_enabled: bool = False):
        super().__init__(app)
        self.profiling_enabled = profiling_enabled
        self.profile_type_to_ext = {"html": "html", "speedscope": "speedscope.json"}
        self.profile_type_to_renderer = {
            "html": HTMLRenderer,
            "speedscope": SpeedscopeRenderer,
        }

    async def dispatch(self, request: Request, call_next: Callable):
        if not self.profiling_enabled or not request.query_params.get("profile", False):
            return await call_next(request)
        profile_type = request.query_params.get("profile_format", "speedscope")
        extension = self.profile_type_to_ext.get(profile_type, "speedscope.json")
        renderer_class = self.profile_type_to_renderer.get(
            profile_type, SpeedscopeRenderer
        )
        with Profiler(interval=0.001, async_mode="enabled") as profiler:
            response = await call_next(request)

        # Write profiling results to file
        output_file = f"profile.{extension}"
        renderer = renderer_class()
        with open(output_file, "w") as out:
            out.write(profiler.output(renderer=renderer))
        return response
