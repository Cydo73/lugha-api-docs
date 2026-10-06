"""A deliberately simple tokenizer.

Real models use learned subword vocabularies. This one cuts every word into
pieces of at most four characters. It is deterministic and easy to explain,
which makes the documentation examples reproducible. It does not describe
how any real model counts tokens.
"""
import math

CHUNK_SIZE = 4


def word_cost(word: str) -> int:
    return math.ceil(len(word) / CHUNK_SIZE)


def count_tokens(text: str) -> int:
    return sum(word_cost(word) for word in text.split())


def truncate_to_tokens(text: str, max_tokens: int) -> tuple[str, int, bool]:
    """Keep whole words until the token budget is used.

    Returns the kept text, the tokens used, and whether text was cut off.
    """
    kept: list[str] = []
    used = 0
    for word in text.split():
        cost = word_cost(word)
        if used + cost > max_tokens:
            return " ".join(kept), used, True
        kept.append(word)
        used += cost
    return " ".join(kept), used, False
