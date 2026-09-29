# Production checklist

Work through this list before you ship. Each item comes from something that goes wrong in real integrations.

## Before you deploy

* [ ] Store API keys in environment variables or a secrets manager, never in source code.
* [ ] Never expose a key in a browser or mobile app. Call the API from your own server.
* [ ] Set a timeout on every request. Without one, a stalled connection can hang your application.
* [ ] Retry `429` and `500` responses and network failures. Do not retry other `4xx` errors.
* [ ] Wait for `Retry-After` on a `429`, and use exponential backoff with a little random jitter for everything else.
* [ ] Log the `request_id` of every failed request so support can find it.
* [ ] Do not log prompts or responses. They may contain personal data.
* [ ] Check `finish_reason`. A value of `length` means the response was cut off.
* [ ] Record `usage.total_tokens` so you can see how much each feature uses.
* [ ] Choose the `region` on purpose and confirm the `X-Data-Region` header matches what you expect.
* [ ] Handle `model_not_found`. Do not assume a model ID will exist forever. List models at startup if you can.
* [ ] Monitor how long requests take, and alert when they get slower.

## A client that follows the list

The repository includes a small Python client that covers the timeout, retry, backoff and logging items. This is its request method.

```{literalinclude} ../examples/python/production_client.py
:language: python
:pyobject: LughaClient._post
```

A few choices worth pointing out:

* It gives up straight away if the server asks for a wait longer than `max_retry_wait`. A request that blocks for a minute is usually worse than a clear failure.
* It logs the status, error type and request ID. It never logs the prompt or the response.
* It only retries statuses in `RETRYABLE_STATUS`. A `400` will not succeed on a second attempt, so the client raises it at once.
