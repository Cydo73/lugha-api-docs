# Lugha Reference API

A small text generation API for African languages, and the developer documentation I wrote for it.

Independent documentation exercise. Lugha is not a real product and is not affiliated with any company. The model is a stub that returns predictable text, so every example in the docs runs and returns exactly what is shown.

## Why I built this

I am applying for API documentation roles and I wanted to show more than writing. So I built a tiny API, ran every example against it, and documented the whole developer journey: get a key, make a first request, read the response, handle errors, and prepare for production.

The interesting part is the docs. The service exists so the docs can be honest.

## What is in here

* `app/` holds the FastAPI service. Four endpoints, one error shape, API key auth and a rate limiter.
* `docs/` holds the documentation, written in Markdown and built with Sphinx and the Furo theme.
* `examples/` holds runnable samples in curl, Python and JavaScript. The docs pull code from these files, so nothing is copied by hand.
* `openapi/openapi.yaml` is exported from the service code. `docs/api-reference.md` is generated from it.
* `tests/` holds the test suite, including a check that the request examples in the reference are accepted by the service.
* `scripts/` holds the two generators.

## Run it locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

The service starts on `http://localhost:8000`. Interactive API pages are at `/docs`.

Try it with the public demo key:

```bash
export LUGHA_API_KEY="lugha_demo_key"
export LUGHA_BASE_URL="http://localhost:8000"
bash examples/curl/quickstart.sh
```

## Run the tests

```bash
python -m pytest -q
```

## Build the docs

```bash
pip install -r docs/requirements.txt
python scripts/export_openapi.py
python scripts/build_reference.py
python -m sphinx -W -b html docs docs/_build/html
```

Open `docs/_build/html/index.html` in a browser. The `-W` flag turns any warning into an error, so a broken link or include fails the build.

## Deploy

1. Push this repository to GitHub.
2. On Render, create a new Blueprint from the repository. It reads `render.yaml` and starts the service. Check that the service URL matches the one in `render.yaml`, and update it if not.
3. Replace `https://YOUR-SERVICE.onrender.com` in `docs/quickstart.md` with your real service URL.
4. On Read the Docs, import the repository. It reads `.readthedocs.yaml` and builds the docs.

## Checks in CI

Every push runs the tests, regenerates the OpenAPI file and the API reference, fails if either is out of date, and builds the docs with warnings as errors.
