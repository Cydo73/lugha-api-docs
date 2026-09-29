"""Lugha Reference API.

A small, honest API used to demonstrate developer documentation for an AI
inference service. The model is a stub, so every example is reproducible.
"""
import uuid

from fastapi import Depends, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import config
from .catalog import MODELS, REGIONS
from .errors import ApiError, error_response
from .schemas import (
    ErrorResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    ModelInfo,
    ModelList,
    TokenCountRequest,
    TokenCountResponse,
    Usage,
)
from .security import authenticate
from .tokenizer import count_tokens, truncate_to_tokens

DESCRIPTION = (
    "Lugha is a reference API for a text generation service that supports African languages. "
    "It exists to demonstrate developer documentation. The model is a stub and the service is "
    "not a real product."
)

TAGS = [
    {"name": "Generation", "description": "Create text with a model."},
    {"name": "Models", "description": "See which models and languages are available."},
    {"name": "Tokens", "description": "Count tokens before you send a request."},
    {"name": "Meta", "description": "Service health."},
]

ERROR_DESCRIPTIONS = {
    400: "The request was invalid. Check the message field.",
    401: "The API key is missing or not valid.",
    404: "The model or endpoint does not exist.",
    429: "Rate limit exceeded. Wait for the number of seconds in the Retry-After header.",
}


def errors(*codes: int) -> dict:
    return {code: {"model": ErrorResponse, "description": ERROR_DESCRIPTIONS[code]} for code in codes}


app = FastAPI(
    title="Lugha Reference API",
    version="1.0.0",
    description=DESCRIPTION,
    openapi_tags=TAGS,
    servers=[{"url": config.PUBLIC_BASE_URL}],
)


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request.state.request_id = "req_" + uuid.uuid4().hex[:12]
    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


@app.exception_handler(ApiError)
async def handle_api_error(request: Request, exc: ApiError):
    return error_response(request, exc.status_code, exc.error_type, exc.message, exc.headers)


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    location = ".".join(str(part) for part in first["loc"] if part != "body")
    message = f"{location}: {first['msg']}" if location else first["msg"]
    return error_response(request, 400, "invalid_request", message)


@app.exception_handler(StarletteHTTPException)
async def handle_http_error(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return error_response(request, 404, "not_found", "There is no endpoint at this path.")
    if exc.status_code == 405:
        return error_response(request, 405, "method_not_allowed", "This endpoint does not accept that HTTP method.")
    return error_response(request, exc.status_code, "http_error", str(exc.detail))


@app.exception_handler(Exception)
async def handle_unexpected_error(request: Request, exc: Exception):
    return error_response(request, 500, "internal_error", "Something went wrong on our side. Quote the request_id if you contact support.")


@app.get("/health", response_model=HealthResponse, tags=["Meta"], summary="Check service health", response_description="The service is running.")
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get(
    "/v1/models",
    response_model=ModelList,
    tags=["Models"],
    summary="List models",
    response_description="The models you can use.",
    responses=errors(401, 429),
)
def list_models(response: Response, _key: str = Depends(authenticate)) -> ModelList:
    return ModelList(data=[ModelInfo(id=name, **details) for name, details in MODELS.items()])


@app.post(
    "/v1/generate",
    response_model=GenerateResponse,
    tags=["Generation"],
    summary="Generate text",
    response_description="The generated text and token usage.",
    description=(
        "Sends a prompt to a model and returns the response. The response includes an "
        "X-Data-Region header that echoes the region that processed the request."
    ),
    responses=errors(400, 401, 404, 429),
)
def generate(body: GenerateRequest, response: Response, _key: str = Depends(authenticate)) -> GenerateResponse:
    model = MODELS.get(body.model)
    if model is None:
        raise ApiError(404, "model_not_found", f"There is no model named '{body.model}'. List models with GET /v1/models.")
    if not body.prompt.strip():
        raise ApiError(400, "invalid_request", "prompt: must contain at least one word.")
    if body.language not in model["languages"]:
        supported = ", ".join(model["languages"])
        raise ApiError(400, "unsupported_language", f"Model '{body.model}' does not support language '{body.language}'. Supported: {supported}.")
    if body.region not in REGIONS:
        raise ApiError(400, "unsupported_region", f"Region '{body.region}' is not available. Choose one of: {', '.join(REGIONS)}.")
    if body.max_tokens > model["max_output_tokens"]:
        raise ApiError(400, "invalid_request", f"max_tokens: must be at most {model['max_output_tokens']} for model '{body.model}'.")

    full_text = f"This is a mock response from {body.model}. Prompt received: {body.prompt}"
    output, completion_tokens, cut_off = truncate_to_tokens(full_text, body.max_tokens)
    prompt_tokens = count_tokens(body.prompt)

    response.headers["X-Data-Region"] = body.region
    return GenerateResponse(
        id="gen_" + uuid.uuid4().hex[:12],
        model=body.model,
        language=body.language,
        output=output,
        finish_reason="length" if cut_off else "stop",
        usage=Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        ),
    )


@app.post(
    "/v1/tokens/count",
    response_model=TokenCountResponse,
    tags=["Tokens"],
    summary="Count tokens",
    response_description="The token count for the text.",
    responses=errors(400, 401, 429),
)
def tokens_count(body: TokenCountRequest, response: Response, _key: str = Depends(authenticate)) -> TokenCountResponse:
    words = len(body.text.split())
    if words == 0:
        raise ApiError(400, "invalid_request", "text: must contain at least one word.")
    tokens = count_tokens(body.text)
    return TokenCountResponse(token_count=tokens, word_count=words, tokens_per_word=round(tokens / words, 2))


def custom_openapi() -> dict:
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=TAGS,
        servers=app.servers,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "description": "Send your API key as: Authorization: Bearer YOUR_API_KEY. The public demo key is lugha_demo_key.",
        }
    }
    for path, methods in schema["paths"].items():
        for operation in methods.values():
            # Validation failures are returned as 400 with the standard error body.
            operation["responses"].pop("422", None)
            if path != "/health":
                operation["security"] = [{"BearerAuth": []}]
    schema["components"]["schemas"].pop("HTTPValidationError", None)
    schema["components"]["schemas"].pop("ValidationError", None)
    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi
