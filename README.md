# Lugha Reference API Documentation

Developer documentation for **Lugha**, a multilingual AI language API designed to make language-aware applications easier to build.

This project demonstrates how I approach **API documentation, developer experience, technical writing, localization, examples, and documentation architecture** for developer-facing products.

## Documentation

**Live documentation:**
`https://YOUR-USERNAME.github.io/lugha-api-docs/`

**Source repository:**
`https://github.com/YOUR-USERNAME/lugha-api-docs`

---

## What this project demonstrates

### API documentation

The documentation covers:

* Authentication
* API endpoints
* Request and response examples
* Error handling
* Production considerations
* Token counting
* Rate limiting
* Usage metadata
* Request IDs
* Data regions
* HTTP status codes

The goal is to make API concepts understandable to developers who need to move from **first request → integration → production** without unnecessary friction.

### Multilingual documentation

The documentation is localized into:

* 🇬🇧 English
* 🇫🇷 French
* 🇵🇹 Portuguese
* 🇰🇪 Kiswahili
* 🇿🇦 Zulu
* 🇳🇬 Yorùbá
* 🇸🇦 Arabic

The documentation uses Sphinx's gettext localization workflow with `.pot` and `.po` translation catalogs.

Arabic is also supported as an RTL language.

### Developer experience

The documentation includes:

* Clear Quickstart guidance
* Copyable API examples
* Syntax-highlighted code
* API reference material
* Error documentation
* Production guidance
* Token usage documentation
* Search-friendly page structure
* Responsive documentation UI
* Dark/light mode support
* Language switching

---

## Documentation architecture

```text
lugha-api-docs/
│
├── docs/
│   ├── index.md
│   ├── quickstart.md
│   ├── authentication.md
│   ├── api-reference.md
│   ├── errors.md
│   ├── production.md
│   ├── tokens.md
│   ├── documentation-decisions.md
│   │
│   ├── locales/
│   │   ├── fr/
│   │   ├── pt/
│   │   ├── sw/
│   │   ├── zu/
│   │   ├── yo/
│   │   └── ar/
│   │
│   └── _static/
│       ├── language-picker.css
│       └── language-picker.js
│
├── examples/
├── openapi/
├── app/
├── scripts/
├── tests/
│
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── .readthedocs.yaml
```

---

## Localization workflow

Translations are managed using Sphinx's gettext workflow.

Source documentation is extracted into translation catalogs:

```bash
python -m sphinx -b gettext docs docs/_build/gettext
```

Translation catalogs are generated with:

```bash
python -m sphinx_intl update \
    -p docs/_build/gettext \
    -d docs/locales \
    -l fr \
    -l pt \
    -l sw \
    -l zu \
    -l yo \
    -l ar
```

Each language maintains its own `.po` catalog while the English documentation remains the source of truth.

---

## Building the documentation locally

### Requirements

* Python 3.11+
* Sphinx
* MyST Parser
* Furo
* sphinx-copybutton
* sphinx-design
* sphinx-intl

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

Build the English documentation:

```bash
python -m sphinx -b html -D language=en docs docs/_build/html
```

Build a translated version:

```bash
python -m sphinx -b html -D language=fr docs docs/_build/html/fr
```

For example:

```bash
python -m sphinx -b html -D language=sw docs docs/_build/html/sw
```

---

## Running locally

After building the documentation:

```bash
python -m http.server 8000 --directory docs/_build/html
```

Then open:

```text
http://localhost:8000
```

The documentation can be tested locally across the supported language versions.

---

## Technology

This project uses:

| Technology        | Purpose                        |
| ----------------- | ------------------------------ |
| **Sphinx**        | Documentation generation       |
| **MyST Markdown** | Markdown-based authoring       |
| **Furo**          | Documentation theme            |
| **sphinx-intl**   | Localization workflow          |
| **gettext**       | Translation catalogs           |
| **Python**        | Documentation tooling          |
| **OpenAPI**       | API specification              |
| **JavaScript**    | Language switching             |
| **CSS**           | Documentation UI customization |

---

## Documentation principles

This project follows several principles when designing developer documentation:

### 1. Optimize for the developer's first successful request

The Quickstart should answer:

> "What do I need to do to make this API work?"

before introducing deeper concepts.

### 2. Separate conceptual and reference documentation

Conceptual explanations explain **why** something works.

Reference documentation explains **exactly what** developers need to send and receive.

Keeping those purposes separate makes documentation easier to navigate.

### 3. Show working examples

API documentation should provide concrete requests and responses rather than relying entirely on prose.

### 4. Document failure paths

Good API documentation should explain what happens when things go wrong.

The error documentation therefore covers authentication failures, invalid requests, unsupported languages, rate limiting, missing resources, and server errors.

### 5. Treat localization as part of developer experience

Translation is not treated as a separate afterthought.

The documentation structure is designed so that localized versions maintain the same information architecture as the English source.

---

## Documentation decisions

The repository includes a dedicated documentation decisions page explaining the reasoning behind the information architecture, API examples, terminology, localization approach, and developer experience choices.

See:

```text
docs/documentation-decisions.md
```

---

## Why I built this

I built Lugha Reference API as a practical demonstration of how I approach **developer documentation for API and developer-tool products**.

Rather than producing isolated writing samples, the project demonstrates the complete documentation workflow:

```text
API concepts
     ↓
Information architecture
     ↓
Developer workflows
     ↓
API reference
     ↓
Code examples
     ↓
Error documentation
     ↓
Production guidance
     ↓
Localization
     ↓
Documentation build
     ↓
Published documentation
```

The objective is to demonstrate not only technical writing ability, but also an understanding of **developer experience and documentation as part of a product**.

---

## Author

**Mumpe Cydrone**

Technical Writer · Developer Documentation · API Documentation

Portfolio: `YOUR_PORTFOLIO_URL`

GitHub: `YOUR_GITHUB_URL`

---

## License

This project is provided for demonstration and portfolio purposes.

