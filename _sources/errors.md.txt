# Errors

When a request fails, the response body always has the same shape, whatever went wrong.

```json
{
  "error": {
    "type": "invalid_request",
    "message": "model: Field required",
    "request_id": "req_502924837fc6"
  }
}
```

`type`
: A machine readable category. Branch your code on this value.

`message`
: A plain explanation for humans. Show it in logs, but do not parse it. The wording can change.

`request_id`
: The ID of this request. It is also in the `X-Request-ID` response header. Quote it when you contact support, and never send your API key.

## Error types

| `type` | Status | What it means | Retry? |
| --- | --- | --- | --- |
| `authentication_required` | 401 | The `Authorization` header is missing or malformed. | No |
| `invalid_api_key` | 401 | The key is not recognised. | No |
| `invalid_request` | 400 | A field is missing or has a bad value. The message names the field. | No |
| `unsupported_language` | 400 | The model does not support this language. The message lists the ones it does. | No |
| `unsupported_region` | 400 | The region is not one of `ke`, `ug`, `ma` or `mu`. | No |
| `model_not_found` | 404 | There is no model with that ID. List models with `GET /v1/models`. | No |
| `not_found` | 404 | There is no endpoint at that path. | No |
| `method_not_allowed` | 405 | The endpoint does not accept that HTTP method. | No |
| `rate_limit_exceeded` | 429 | You used all your requests for this minute. | Yes, after `Retry-After` |
| `internal_error` | 500 | Something went wrong on the service side. | Yes, with backoff |

A `400`, `401`, `404` or `405` means the request itself needs to change. Sending it again unchanged will fail again.

## Examples

A model that does not support the language you asked for:

```json
{
  "error": {
    "type": "unsupported_language",
    "message": "Model 'lugha-demo-small' does not support language 'am'. Supported: en, sw, lg.",
    "request_id": "req_183e64b5682b"
  }
}
```

The fix is in the message. Use a model that supports the language, or choose one of the listed languages.

## Rate limits

Each API key can make 10 requests per minute. The count resets at the start of each minute. Every response tells you where you stand.

| Header | Meaning |
| --- | --- |
| `X-RateLimit-Limit` | Requests allowed per minute. |
| `X-RateLimit-Remaining` | Requests left in the current minute. |
| `X-RateLimit-Reset` | Seconds until the count resets. |

When you use up your requests, the next one returns status `429` with a `Retry-After` header.

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 60
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 60
X-Request-ID: req_658e47454555
```

```json
{
  "error": {
    "type": "rate_limit_exceeded",
    "message": "You have used all 10 requests for this minute. Retry in 60 seconds.",
    "request_id": "req_658e47454555"
  }
}
```

Wait for the number of seconds in `Retry-After`, then send the request again. Retrying straight away only uses up more of your allowance.

If you see `429` often, slow your requests down. Watch `X-RateLimit-Remaining` and pause before it reaches zero.

## What to retry

Retry `429` after the `Retry-After` delay. Retry `500` and network failures with exponential backoff, which means waiting a little longer after each failed attempt. Never retry the other errors.

The [production checklist](production.md) includes a client that does all of this.
