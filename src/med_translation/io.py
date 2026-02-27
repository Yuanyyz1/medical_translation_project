from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


def read_excel_records(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    frame = pd.read_excel(path)
    return frame.to_dict(orient="records")


def write_excel_records(records: Iterable[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(list(records))
    frame.to_excel(path, index=False)


def write_dataframe(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False)
