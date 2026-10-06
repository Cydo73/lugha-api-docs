"""A small client that follows the production checklist.

It sets timeouts, retries only errors that are worth retrying, waits the amount
the server asks for, logs request IDs, and never logs prompts or responses.
"""
import logging
import os
import random
import time

import requests

log = logging.getLogger("lugha")

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class LughaError(Exception):
    def __init__(self, status: int, error_type: str, message: str, request_id: str):
        super().__init__(f"{error_type}: {message} (request_id={request_id})")
        self.status = status
        self.error_type = error_type
        self.request_id = request_id


class LughaClient:
    def __init__(self, base_url=None, api_key=None, timeout=30, max_retries=3, max_retry_wait=20, session=None):
        self.base_url = (base_url or os.environ.get("LUGHA_BASE_URL", "http://localhost:8000")).rstrip("/")
        self.api_key = api_key or os.environ["LUGHA_API_KEY"]
        self.timeout = timeout
        self.max_retries = max_retries
        self.max_retry_wait = max_retry_wait
        self.session = session or requests.Session()

    def generate(self, **body) -> dict:
        return self._post("/v1/generate", body)

    def _post(self, path: str, body: dict) -> dict:
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.post(
                    f"{self.base_url}{path}",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=body,
                    timeout=self.timeout,
                )
            except requests.exceptions.RequestException as exc:
                # Network failures and timeouts are worth retrying.
                if attempt == self.max_retries:
                    raise
                self._sleep(attempt, None, f"network error {type(exc).__name__}")
                continue

            if response.status_code < 400:
                return response.json()

            error = response.json().get("error", {})
            failure = LughaError(
                response.status_code,
                error.get("type", "unknown"),
                error.get("message", ""),
                error.get("request_id", response.headers.get("X-Request-ID", "unknown")),
            )
            log.warning("Request failed: status=%s type=%s request_id=%s", failure.status, failure.error_type, failure.request_id)

            if response.status_code not in RETRYABLE_STATUS or attempt == self.max_retries:
                raise failure

            retry_after = response.headers.get("Retry-After")
            if retry_after and float(retry_after) > self.max_retry_wait:
                raise failure
            self._sleep(attempt, retry_after, f"status {response.status_code}")

        raise RuntimeError("unreachable")

    def _sleep(self, attempt: int, retry_after, reason: str) -> None:
        if retry_after:
            delay = float(retry_after)
        else:
            delay = min(2 ** attempt, self.max_retry_wait) + random.uniform(0, 0.5)
        log.info("Retrying in %.1fs after %s", delay, reason)
        time.sleep(delay)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    client = LughaClient()
    result = client.generate(model="lugha-demo-large", prompt="Habari ya asubuhi", language="sw")
    print(result["usage"])
