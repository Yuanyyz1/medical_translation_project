from __future__ import annotations

import re
from collections import Counter
from typing import Iterable


def word_count(text) -> int:
    if text is None:
        return 0
    if isinstance(text, list):
        text = " ".join(str(item) for item in text)
    if not isinstance(text, str):
        text = str(text)
    return len(text.split())


def counter_summary(data: list[dict], fields: list[str]) -> Counter:
    return Counter(
        item.get(field)
        for item in data
        for field in fields
        if item.get(field)
    )


def counter_summary_clean(data: list[dict], fields: list[str], clean: bool = True) -> list[tuple[str, int]]:
    counter = counter_summary(data, fields)
    if not clean:
        return sorted(counter.items(), key=lambda x: x[1], reverse=True)

    merged: dict[str, int] = {}
    for key, value in counter.items():
        normalized = re.sub(r"\s*\([^)]*\)", "", key)
        merged[normalized] = merged.get(normalized, 0) + value

    return sorted(merged.items(), key=lambda x: x[1], reverse=True)


def require_keys(item: dict, keys: Iterable[str]) -> None:
    missing = [key for key in keys if key not in item]
    if missing:
        raise KeyError(f"Missing required keys: {missing}")
