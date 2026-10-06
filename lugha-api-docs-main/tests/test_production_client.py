import importlib.util
import pathlib

import pytest
import requests

spec = importlib.util.spec_from_file_location(
    "production_client",
    pathlib.Path(__file__).resolve().parent.parent / "examples" / "python" / "production_client.py",
)
production_client = importlib.util.module_from_spec(spec)
spec.loader.exec_module(production_client)


class FakeResponse:
    def __init__(self, status_code, body, headers=None):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}

    def json(self):
        return self._body


class FakeSession:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def post(self, *args, **kwargs):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def make_client(outcomes, **kwargs):
    session = FakeSession(outcomes)
    client = production_client.LughaClient(base_url="http://x", api_key="k", session=session, **kwargs)
    return client, session


def rate_limited(retry_after="1"):
    body = {"error": {"type": "rate_limit_exceeded", "message": "slow down", "request_id": "req_1"}}
    return FakeResponse(429, body, {"Retry-After": retry_after})


def test_retries_after_429_and_succeeds(monkeypatch):
    slept = []
    monkeypatch.setattr(production_client.time, "sleep", slept.append)
    client, session = make_client([rate_limited("2"), FakeResponse(200, {"output": "ok"})])
    assert client.generate(model="m", prompt="p") == {"output": "ok"}
    assert session.calls == 2
    assert slept == [2.0]


def test_does_not_retry_a_bad_request(monkeypatch):
    monkeypatch.setattr(production_client.time, "sleep", lambda _s: None)
    body = {"error": {"type": "invalid_request", "message": "model: Field required", "request_id": "req_2"}}
    client, session = make_client([FakeResponse(400, body)])
    with pytest.raises(production_client.LughaError) as info:
        client.generate(prompt="p")
    assert info.value.error_type == "invalid_request"
    assert info.value.request_id == "req_2"
    assert session.calls == 1


def test_gives_up_when_server_asks_for_a_long_wait(monkeypatch):
    monkeypatch.setattr(production_client.time, "sleep", lambda _s: None)
    client, session = make_client([rate_limited("50")], max_retry_wait=10)
    with pytest.raises(production_client.LughaError) as info:
        client.generate(model="m", prompt="p")
    assert info.value.status == 429
    assert session.calls == 1


def test_retries_network_errors(monkeypatch):
    monkeypatch.setattr(production_client.time, "sleep", lambda _s: None)
    client, session = make_client([requests.exceptions.Timeout(), FakeResponse(200, {"output": "ok"})])
    assert client.generate(model="m", prompt="p")["output"] == "ok"
    assert session.calls == 2
