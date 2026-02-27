from __future__ import annotations

import logging
from typing import Callable

from ..utils import require_keys

logger = logging.getLogger(__name__)

DETECTION_INPUT_FIELDS = [
    "case_turn_id",
    "setting_short",
    "speaker",
    "en_1",
    "cn_2_1",
    "cn_1",
    "en_2_1",
    "errors_1",
    "errors_domain_1",
    "errors_explain_1",
]

DETECTION_OUTPUT_FIELDS = [
    "errors_detected_text1",
    "errors_detected_domain_text1",
    "errors_detected_domain_explain_text1",
    "clinical_consequences_explain_text1",
    "clinical_consequences_flag_text1",
    "errors_detected_text2",
    "errors_detected_domain_text2",
    "errors_detected_domain_explain_text2",
    "clinical_consequences_explain_text2",
    "clinical_consequences_flag_text2",
    "ambiguity",
]


def build_detection_inputs(insertion_rows: list[dict]) -> list[dict]:
    detection_rows = []
    for row in insertion_rows:
        require_keys(row, DETECTION_INPUT_FIELDS)
        detection_rows.append({field: row[field] for field in DETECTION_INPUT_FIELDS})
    return detection_rows


def run_error_detection(
    rows: list[dict],
    predictor: Callable | None = None,
    log_every: int = 10,
) -> list[dict]:
    if predictor is None:
        import dspy

        from ..signatures import DetectError

        predictor = dspy.Predict(DetectError)
    output: list[dict] = []

    for idx, row in enumerate(rows, start=1):
        require_keys(row, ["en_1", "cn_2_1", "cn_1", "en_2_1"])
        result = predictor(
            en_1=row["en_1"],
            cn_2_1=row["cn_2_1"],
            cn_1=row["cn_1"],
            en_2_1=row["en_2_1"],
        )

        extracted = {field: getattr(result, field, None) for field in DETECTION_OUTPUT_FIELDS}
        if not any(value is not None for value in extracted.values()):
            completions = getattr(result, "_completions", None)
            if completions:
                store = getattr(completions[0], "_store", {})
                for field in DETECTION_OUTPUT_FIELDS:
                    extracted[field] = store.get(field)

        output.append(row | extracted)

        if idx % log_every == 0 or idx == len(rows):
            logger.info("error detection progress: %s/%s", idx, len(rows))

    return output


def run_detection_for_models(
    rows: list[dict],
    model_names: list[str],
    registry,
) -> dict[str, list[dict]]:
    results: dict[str, list[dict]] = {}
    for model_name in model_names:
        with registry.model_context(model_name):
            results[model_name] = run_error_detection(rows)
    return results
