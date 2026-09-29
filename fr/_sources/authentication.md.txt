# Authentication

Every endpoint except `/health` needs an API key. Send it in the `Authorization` header as a bearer token.

```text
Authorization: Bearer YOUR_API_KEY
```

The public demo key is `lugha_demo_key`. It is shared and rate limited, so use it for trying things out and nothing else.

## Keep your key out of your code

Read the key from an environment variable.

```python
import os

api_key = os.environ["LUGHA_API_KEY"]
```

Three rules keep keys safe.

* Never commit a key to source control. Add any file that holds a key, such as `.env`, to `.gitignore`.
* Never put a key in code that runs in a browser or a mobile app. Anyone can read it. Call the API from your own server instead.
* Never paste a key into a support message. Send the `request_id` from the error instead.

## Rotate keys without downtime

The service accepts more than one key at a time. To rotate:

1. Add the new key alongside the old one.
2. Deploy your applications with the new key.
3. Remove the old key once nothing uses it.

If a key leaks, remove it straight away and issue a new one.

## Authentication errors

Both authentication failures return status `401`.

| `type` | Cause | What to do |
| --- | --- | --- |
| `authentication_required` | The `Authorization` header is missing, or it does not start with `Bearer`. | Add the header in the format above. |
| `invalid_api_key` | The header is well formed but the key is not recognised. | Check for typos, extra spaces and expired keys. |

Do not retry a `401`. The same request will fail the same way.

```json
{
  "error": {
    "type": "authentication_required",
    "message": "Send your API key in the Authorization header as: Bearer YOUR_API_KEY.",
    "request_id": "req_cd80844c370a"
  }
}
```
