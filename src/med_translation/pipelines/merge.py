from __future__ import annotations

import pandas as pd

from .error_detection import DETECTION_OUTPUT_FIELDS


def merge_detection_results(base_rows: list[dict], detection_by_model: dict[str, list[dict]]) -> pd.DataFrame:
    base_df = pd.DataFrame(base_rows).reset_index(drop=True)
    frames = [base_df]

    for model_name, rows in detection_by_model.items():
        frame = pd.DataFrame(rows).reset_index(drop=True)
        missing = [col for col in DETECTION_OUTPUT_FIELDS if col not in frame.columns]
        if missing:
            raise ValueError(f"Model '{model_name}' is missing required detection columns: {missing}")
        frames.append(frame[DETECTION_OUTPUT_FIELDS].add_suffix(f"_{model_name}"))

    return pd.concat(frames, axis=1)
