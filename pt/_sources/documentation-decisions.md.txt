# Documentation decisions

I wrote these pages as a sample of how I document an API for developers. This page explains the choices, so you can judge my thinking as well as my writing.

## Why the quickstart comes first

Someone evaluating an API wants proof that it works before they read anything else. The quickstart gets a real request running in a few minutes, then explains every field in the response. Every other page links back to it.

## Why the examples are real files

The code on these pages is pulled straight from the `examples` folder. I ran each one against the running service: curl, Python and JavaScript. The docs show exactly the code that ran, and there is no second copy to go stale. Sample code that drifts away from the docs is one of the most common ways developer documentation stops being trusted.

## Why errors get their own page

Errors are where developers spend most of their debugging time. Every failure uses one shape, with a `type` to branch on, a `message` for people and a `request_id` for support. The table says which errors are worth retrying, because that is the question a developer actually has at that moment.

## Why the reference is generated

The API reference comes from `openapi/openapi.yaml`, and that file is exported from the service code. The continuous integration check fails if the file is out of date. I would rather explain the API in prose and let a tool list the parameters, because copying parameters by hand is how references end up wrong.

## Why the model is a stub

I do not have a real model, and inventing behaviour I cannot verify would make these docs untrustworthy. The stub returns predictable text, so every response on these pages is exactly what you get if you run the request. The tokenizer is simple for the same reason, and the tokens page says so plainly.

## Why tokens and regions get attention

For developers building in African languages, two questions come up early: how many tokens their text will use, and where their data is processed. I added a token counting endpoint and a `region` parameter to give those questions a place in the documentation. They are illustrative design choices for this sample, not claims about any real service.

## What I left out on purpose

I left out streaming, official SDK packages, billing and pagination. A small set of pages done properly is more useful than a large set done quickly. Streaming would be my next addition, because it changes what a quickstart looks like.

## What I would do with a real product

I would sit with the engineers and read the code before writing a word. I would run every example myself, and I would use support tickets and usage data to decide what to document first. I would also keep a changelog, so developers can see what changed between versions.
