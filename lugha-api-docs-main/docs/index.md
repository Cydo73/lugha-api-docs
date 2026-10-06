# Lugha Reference API

Lugha is a small text generation API that supports African languages. Use it to generate text, count tokens before you send a request, and choose the region that processes your data.

```{admonition} Independent documentation exercise
:class: note

Lugha is not a real product. It is a reference API written to show how I document an AI inference service for developers. The model is a stub that returns predictable text, so every example on these pages runs and returns exactly what is shown.

Source code: [Lugha on GitHub](https://github.com/Cydo73/lugha-api-docs)
```

## Start here

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} Quickstart
:link: quickstart
:link-type: doc

Make your first request in about five minutes.
:::

:::{grid-item-card} Handle errors
:link: errors
:link-type: doc

Every error has a type, a message and a request ID. Learn what to do with each one.
:::

:::{grid-item-card} Go to production
:link: production
:link-type: doc

A checklist to work through before you ship.
:::

:::{grid-item-card} API reference
:link: api-reference
:link-type: doc

Every endpoint, parameter and response.
:::
::::

```{toctree}
:hidden:
:maxdepth: 1

quickstart
authentication
tokens
errors
production
api-reference
documentation-decisions
```
