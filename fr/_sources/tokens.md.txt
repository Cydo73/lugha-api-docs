# Tokens and languages

Models do not read words. They read tokens, which are pieces of text. You pay for tokens, your `max_tokens` limit is measured in tokens, and longer token counts take longer to process. So it helps to know how many tokens your text will use before you send it.

## Why the same idea can cost different amounts

A tokenizer that was built mostly around English text often cuts words from other languages into more pieces. The same sentence in two languages can therefore use a different number of tokens, even when the meaning is identical. If you build for several languages, check token counts for each one instead of assuming they match.

## Count tokens before you send

`POST /v1/tokens/count` returns the token count for a piece of text.

```{note}
Lugha uses a deliberately simple tokenizer. It cuts every word into pieces of at most four characters. That makes results easy to explain and reproduce. It does not describe how any real model counts tokens, so treat the numbers below as a demonstration of the endpoint, not a measurement.
```

Count an English sentence:

```bash
curl "$LUGHA_BASE_URL/v1/tokens/count" \
  -H "Authorization: Bearer $LUGHA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Good morning, my friend."}'
```

```json
{"token_count": 6, "word_count": 4, "tokens_per_word": 1.5}
```

Now a Swahili sentence:

```bash
curl "$LUGHA_BASE_URL/v1/tokens/count" \
  -H "Authorization: Bearer $LUGHA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Habari ya asubuhi, rafiki yangu."}'
```

```json
{"token_count": 9, "word_count": 5, "tokens_per_word": 1.8}
```

`token_count`
: The number of tokens in the text.

`word_count`
: The number of words, split on whitespace.

`tokens_per_word`
: `token_count` divided by `word_count`, rounded to two decimals. Use it to compare texts of different lengths.

## How tokens show up elsewhere

The `usage` object in a `/v1/generate` response reports the same counts for a real request: `prompt_tokens` for what you sent and `completion_tokens` for what came back.

`max_tokens` limits `completion_tokens` only. It does not include your prompt. If the model reaches the limit, the response ends with `finish_reason` set to `length`.

Count your prompt first if you want to estimate the size of a request before you make it.
