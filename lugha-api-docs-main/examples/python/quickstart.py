import os

import requests

BASE_URL = os.environ.get("LUGHA_BASE_URL", "http://localhost:8000")
API_KEY = os.environ["LUGHA_API_KEY"]

response = requests.post(
    f"{BASE_URL}/v1/generate",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "lugha-demo-large",
        "prompt": "Explain Kampala to a developer visiting Uganda for the first time.",
        "language": "en",
        "max_tokens": 64,
        "region": "ug",
    },
    timeout=30,
)
response.raise_for_status()

data = response.json()
print(data["output"])
print("Tokens used:", data["usage"]["total_tokens"])
