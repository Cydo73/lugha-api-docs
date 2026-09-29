# Quickstart

Make your first request and read the response in about five minutes.

You need one of these on your machine: `curl`, Python 3.9 or later with the `requests` package, or Node.js 18 or later. Nothing else to install.

## 1. Set your environment

Your API key and the server address live in environment variables, so they never end up in your code.

The demo key below is public. It is limited to 10 requests per minute.

```bash
export LUGHA_API_KEY="lugha_demo_key"
export LUGHA_BASE_URL="https://YOUR-SERVICE.onrender.com"
```

```{note}
If the demo server has been idle, the first request can take up to a minute to respond. Later requests are fast.
```

## 2. Send your first request

Ask the large model a question. Pick the tab for your language.

::::{tab-set}

:::{tab-item} curl
```{literalinclude} ../examples/curl/quickstart.sh
:language: bash
:lines: 4-
```
:::

:::{tab-item} Python
```{literalinclude} ../examples/python/quickstart.py
:language: python
```
:::

:::{tab-item} JavaScript
```{literalinclude} ../examples/javascript/quickstart.mjs
:language: javascript
```
:::

::::

## 3. Read the response

A successful request returns status `200` and a JSON body like this. Your `id` will differ.

```json
{
  "id": "gen_955dad72d7bd",
  "model": "lugha-demo-large",
  "language": "en",
  "output": "This is a mock response from lugha-demo-large. Prompt received: Explain Kampala to a developer visiting Uganda for the first time.",
  "finish_reason": "stop",
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 36,
    "total_tokens": 55
  }
}
```

The model is a stub, so `output` repeats your prompt inside a fixed sentence. That keeps every example on these pages reproducible. The shape of the response is what matters here.

`id`
: A unique ID for this generation. Log it if you need to refer to the generation later.

`model`
: The model that handled the request.

`language`
: The language code you sent. If you leave it out, it defaults to `en`.

`output`
: The generated text.

`finish_reason`
: Why the response ended. `stop` means it finished naturally. `length` means it hit your `max_tokens` limit and was cut off.

`usage`
: How many tokens the request used. `total_tokens` is `prompt_tokens` plus `completion_tokens`. See [Tokens and languages](tokens.md) for how tokens are counted.

### When the response is cut off

Set `max_tokens` to 10 and send the same prompt. The output stops early and `finish_reason` changes to `length`.

```json
{
  "id": "gen_6b8a83382d2d",
  "model": "lugha-demo-large",
  "language": "en",
  "output": "This is a mock response from",
  "finish_reason": "length",
  "usage": {
    "prompt_tokens": 19,
    "completion_tokens": 7,
    "total_tokens": 26
  }
}
```

If you see `length` and you expected a full answer, raise `max_tokens`. Each model has its own ceiling, listed under `max_output_tokens` in the [model list](#choose-a-model-and-language).

### Response headers

Every response carries headers worth knowing about.

| Header | Meaning |
| --- | --- |
| `X-Request-ID` | Unique ID for this request. Quote it when you contact support. |
| `X-Data-Region` | The region that processed the request. Only on `/v1/generate`. |
| `X-RateLimit-Limit` | How many requests you get per minute. |
| `X-RateLimit-Remaining` | How many you have left in the current minute. |
| `X-RateLimit-Reset` | Seconds until the counter resets. |

## Choose a model and language

List the models to see which languages each one accepts.

```bash
curl "$LUGHA_BASE_URL/v1/models" -H "Authorization: Bearer $LUGHA_API_KEY"
```

```json
{
  "data": [
    {
      "id": "lugha-demo-small",
      "max_output_tokens": 128,
      "languages": ["en", "sw", "lg"]
    },
    {
      "id": "lugha-demo-large",
      "max_output_tokens": 512,
      "languages": ["en", "sw", "ha", "yo", "lg", "am"]
    }
  ]
}
```

The language codes are `en` English, `sw` Swahili, `ha` Hausa, `yo` Yoruba, `lg` Luganda and `am` Amharic. If you send a language the model does not support, you get an `unsupported_language` error that lists the ones it does. See [Errors](errors.md).

## Choose a region

The `region` parameter tells the service where to process your request. Use `ke` for Kenya, `ug` for Uganda, `ma` for Morocco or `mu` for Mauritius. If you leave it out, the default is `ke`. The `X-Data-Region` response header confirms where the request ran.

## Next steps

* [Authentication](authentication.md) explains keys in more detail.
* [Errors](errors.md) covers every error and which ones to retry.
* [Production checklist](production.md) is what to review before you ship.
