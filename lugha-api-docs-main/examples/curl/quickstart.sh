#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${LUGHA_BASE_URL:-http://localhost:8000}"
API_KEY="${LUGHA_API_KEY:?Set LUGHA_API_KEY first}"

curl "$BASE_URL/v1/generate" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "lugha-demo-large",
    "prompt": "Explain Kampala to a developer visiting Uganda for the first time.",
    "language": "en",
    "max_tokens": 64,
    "region": "ug"
  }'
