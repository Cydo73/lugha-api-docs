"""One error shape for every failure: type, message and request_id."""
from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, status_code: int, error_type: str, message: str, headers: dict | None = None):
        self.status_code = status_code
        self.error_type = error_type
        self.message = message
        self.headers = headers or {}


def error_response(request: Request, status_code: int, error_type: str, message: str, headers: dict | None = None):
    request_id = getattr(request.state, "request_id", "req_unknown")
    response_headers = {"X-Request-ID": request_id, **(headers or {})}
    return JSONResponse(
        status_code=status_code,
        content={"error": {"type": error_type, "message": message, "request_id": request_id}},
        headers=response_headers,
    )
