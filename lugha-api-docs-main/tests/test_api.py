import pytest
from fastapi.testclient import TestClient

from app import config, security
from app.main import app

AUTH = {"Authorization": "Bearer lugha_demo_key"}


@pytest.fixture(autouse=True)
def clean_state(monkeypatch):
    security.reset_rate_limits()
    monkeypatch.setattr(config, "RATE_LIMIT_PER_MINUTE", 100)
    yield
    security.reset_rate_limits()


@pytest.fixture
def client():
    return TestClient(app)


def generate(client, **overrides):
    body = {"model": "lugha-demo-large", "prompt": "Hello from Kampala"}
    body.update(overrides)
    return client.post("/v1/generate", json=body, headers=AUTH)


def assert_error(response, status, error_type):
    assert response.status_code == status
    error = response.json()["error"]
    assert error["type"] == error_type
    assert error["request_id"].startswith("req_")
    assert response.headers["X-Request-ID"] == error["request_id"]
    return error


def test_health_needs_no_key(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_missing_key(client):
    assert_error(client.get("/v1/models"), 401, "authentication_required")


def test_wrong_key(client):
    response = client.get("/v1/models", headers={"Authorization": "Bearer nope"})
    assert_error(response, 401, "invalid_api_key")


def test_list_models(client):
    response = client.get("/v1/models", headers=AUTH)
    assert response.status_code == 200
    ids = [model["id"] for model in response.json()["data"]]
    assert ids == ["lugha-demo-small", "lugha-demo-large"]


def test_generate_success(client):
    response = generate(client, language="en", region="ug")
    assert response.status_code == 200
    body = response.json()
    assert body["id"].startswith("gen_")
    assert body["finish_reason"] == "stop"
    assert body["usage"]["total_tokens"] == body["usage"]["prompt_tokens"] + body["usage"]["completion_tokens"]
    assert response.headers["X-Data-Region"] == "ug"
    assert response.headers["X-Request-ID"].startswith("req_")


def test_generate_is_cut_off_at_max_tokens(client):
    response = generate(client, max_tokens=5)
    body = response.json()
    assert body["finish_reason"] == "length"
    assert body["usage"]["completion_tokens"] <= 5


def test_unknown_model(client):
    assert_error(generate(client, model="nope"), 404, "model_not_found")


def test_unsupported_language_for_model(client):
    error = assert_error(generate(client, model="lugha-demo-small", language="am"), 400, "unsupported_language")
    assert "en, sw, lg" in error["message"]


def test_unsupported_region(client):
    assert_error(generate(client, region="zz"), 400, "unsupported_region")


def test_max_tokens_above_model_limit(client):
    error = assert_error(generate(client, model="lugha-demo-small", max_tokens=500), 400, "invalid_request")
    assert "128" in error["message"]


def test_missing_required_field(client):
    response = client.post("/v1/generate", json={"prompt": "hi"}, headers=AUTH)
    error = assert_error(response, 400, "invalid_request")
    assert error["message"].startswith("model:")


def test_blank_prompt(client):
    assert_error(generate(client, prompt="   "), 400, "invalid_request")


def test_token_count(client):
    response = client.post("/v1/tokens/count", json={"text": "Habari ya asubuhi"}, headers=AUTH)
    assert response.status_code == 200
    # Habari = 6 letters = 2 tokens, ya = 1, asubuhi = 7 letters = 2
    assert response.json() == {"token_count": 5, "word_count": 3, "tokens_per_word": 1.67}


def test_token_count_blank_text(client):
    response = client.post("/v1/tokens/count", json={"text": "   "}, headers=AUTH)
    assert_error(response, 400, "invalid_request")


def test_unknown_path(client):
    assert_error(client.get("/v1/nothing", headers=AUTH), 404, "not_found")


def test_wrong_method(client):
    assert_error(client.get("/v1/generate", headers=AUTH), 405, "method_not_allowed")


def test_rate_limit(client, monkeypatch):
    monkeypatch.setattr(config, "RATE_LIMIT_PER_MINUTE", 2)
    first = client.get("/v1/models", headers=AUTH)
    assert first.headers["X-RateLimit-Remaining"] == "1"
    client.get("/v1/models", headers=AUTH)
    blocked = client.get("/v1/models", headers=AUTH)
    assert_error(blocked, 429, "rate_limit_exceeded")
    assert int(blocked.headers["Retry-After"]) >= 1
    assert blocked.headers["X-RateLimit-Remaining"] == "0"


def test_unexpected_error_uses_standard_shape(monkeypatch):
    def boom(_text):
        raise RuntimeError("boom")

    monkeypatch.setattr("app.main.count_tokens", boom)
    quiet_client = TestClient(app, raise_server_exceptions=False)
    response = quiet_client.post("/v1/tokens/count", json={"text": "hello"}, headers=AUTH)
    assert_error(response, 500, "internal_error")


def test_openapi_has_no_422_and_lists_bearer_auth(client):
    schema = client.get("/openapi.json").json()
    assert "BearerAuth" in schema["components"]["securitySchemes"]
    for methods in schema["paths"].values():
        for operation in methods.values():
            assert "422" not in operation["responses"]


def test_documented_request_examples_work(client):
    """The example bodies shown in the API reference must be accepted by the service."""
    import sys
    import pathlib

    scripts = pathlib.Path(__file__).resolve().parent.parent / "scripts"
    sys.path.insert(0, str(scripts))
    from build_reference import example_request

    schemas = client.get("/openapi.json").json()["components"]["schemas"]
    generate_example = example_request("GenerateRequest", schemas)
    assert client.post("/v1/generate", json=generate_example, headers=AUTH).status_code == 200
    tokens_example = example_request("TokenCountRequest", schemas)
    assert client.post("/v1/tokens/count", json=tokens_example, headers=AUTH).status_code == 200
