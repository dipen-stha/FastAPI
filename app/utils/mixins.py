import typing
import json

from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask


class CustomResponse(JSONResponse):
    def __init__(self,
        content: typing.Any,
        message: str | None = None,
        data: dict | list[dict] | None = None,
        status_code: int = 200,
        headers: typing.Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,):
        super().__init__()

    def render(self, content: typing.Any) -> bytes:
        content['message'] = self.message
        content['data'] = self.data
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
