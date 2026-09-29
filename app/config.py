"""Runtime settings, read from environment variables."""
import os

# Comma separated list of valid API keys. The public demo key is documented on purpose.
API_KEYS = {
    key.strip()
    for key in os.getenv("LUGHA_API_KEYS", "lugha_demo_key").split(",")
    if key.strip()
}

# Requests allowed per API key in each 60 second window.
RATE_LIMIT_PER_MINUTE = int(os.getenv("LUGHA_RATE_LIMIT_PER_MINUTE", "10"))

# Used only to fill in the OpenAPI "servers" list.
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")
