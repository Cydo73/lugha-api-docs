# Quickstart

Make your first request and read the response in about five minutes.

To run the service you need Git and Python 3.9 or later. To send requests you need one of these: curl, PowerShell (built into Windows), Python with the `requests` package, or Node.js 18 or later.

## 1. Start the service

Lugha is a small service that runs on your own computer, so you can follow every example without signing up for anything. Open a terminal and run these commands. Pick the tab for your system.

::::{tab-set}

:::{tab-item} macOS and Linux
:sync: unix
```bash
git clone https://github.com/Cydo73/lugha-api-docs.git
cd lugha-api-docs
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app
```
:::

:::{tab-item} Windows PowerShell
:sync: windows
```powershell
git clone https://github.com/Cydo73/lugha-api-docs.git
cd lugha-api-docs
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app
```

```{note}
If activation fails with "running scripts is disabled on this system", run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned` and activate again. The change only lasts for this window.
```
:::

::::

When the service is ready, the terminal prints a line that ends with `Uvicorn running on http://127.0.0.1:8000`. Leave this window open, because the service stops when you close it. Open a second terminal window for the rest of this page.

Check that the service is running:

::::{tab-set}

:::{tab-item} macOS and Linux
:sync: unix
```bash
curl http://localhost:8000/health
```
:::

:::{tab-item} Windows PowerShell
:sync: windows
```powershell
Invoke-RestMethod http://localhost:8000/health | ConvertTo-Json -Compress
```
:::

::::

You should see `{"status":"ok"}`.

## 2. Set your environment

Your API key and the server address live in environment variables, so they never end up in your code. Run these in your second terminal window.

The demo key below is public. It is limited to 10 requests per minute.

::::{tab-set}

:::{tab-item} macOS and Linux
:sync: unix
```bash
export LUGHA_API_KEY="lugha_demo_key"
export LUGHA_BASE_URL="http://localhost:8000"
```
:::

:::{tab-item} Windows PowerShell
:sync: windows
```powershell
$env:LUGHA_API_KEY = "lugha_demo_key"
$env:LUGHA_BASE_URL = "http://localhost:8000"
```
:::

::::

```{note}
These settings last only for the window where you ran them. If you open a new window, set them again.
```

## 3. Send your first request

Ask the large model a question. Each example is a file in the `examples` folder of the repository you cloned. In your second window, go to the repository folder, then paste the code or run the file. Pick the tab for your language.

::::{tab-set}

:::{tab-item} curl
```{literalinclude} ../examples/curl/quickstart.sh
:language: bash
:lines: 4-
```

Or run the file:

```bash
bash examples/curl/quickstart.sh
```
:::

:::{tab-item} PowerShell
```{literalinclude} ../examples/powershell/quickstart.ps1
:language: powershell
```

Or run the file:

```powershell
.\examples\powershell\quickstart.ps1
```
:::

:::{tab-item} Python
```{literalinclude} ../examples/python/quickstart.py
:language: python
```

Install the `requests` package once, then run the file. Use `python` on Windows and `python3` on macOS and Linux.

```bash
pip install requests
python3 examples/python/quickstart.py
```
:::

:::{tab-item} JavaScript
```{literalinclude} ../examples/javascript/quickstart.mjs
:language: javascript
```

Run the file:

```bash
node examples/javascript/quickstart.mjs
```
:::

::::

## 4. Read the response

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

::::{tab-set}

:::{tab-item} macOS and Linux
:sync: unix
```bash
curl "$LUGHA_BASE_URL/v1/models" -H "Authorization: Bearer $LUGHA_API_KEY"
```
:::

:::{tab-item} Windows PowerShell
:sync: windows
```powershell
Invoke-RestMethod "$env:LUGHA_BASE_URL/v1/models" -Headers @{ Authorization = "Bearer $env:LUGHA_API_KEY" } | ConvertTo-Json -Depth 5
```
:::

::::

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
