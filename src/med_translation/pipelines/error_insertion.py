from __future__ import annotations

import logging
from typing import Callable

from ..types import ConversationRow
from ..utils import require_keys, word_count

logger = logging.getLogger(__name__)

INSERTION_OUTPUT_FIELDS = [
    "errors_1",
    "errors_domain_1",
    "errors_explain_1",
    "en_2_1",
    "cn_2_1",
    "errors_2",
    "errors_domain_2",
    "errors_explain_2",
    "en_2_2",
    "cn_2_2",
    "errors_3",
    "errors_domain_3",
    "errors_explain_3",
    "en_2_3",
    "cn_2_3",
    "error_best",
    "error_best_explain",
    "ambiguity",
]


def filter_long_rows(rows: list[ConversationRow], min_words: int = 5) -> list[ConversationRow]:
    return [
        row
        for row in rows
        if isinstance(row.get("text"), str) and word_count(row.get("text")) > min_words
    ]


def run_error_insertion(
    rows: list[ConversationRow],
    pharmacist_predictor: Callable | None = None,
    patient_predictor: Callable | None = None,
    log_every: int = 10,
) -> list[dict]:
    if pharmacist_predictor is None or patient_predictor is None:
        import dspy

        from ..signatures import InsertErrorPatient, InsertErrorPharmacist

        pharmacist_predictor = pharmacist_predictor or dspy.Predict(InsertErrorPharmacist)
        patient_predictor = patient_predictor or dspy.Predict(InsertErrorPatient)

    output: list[dict] = []
    for idx, row in enumerate(rows, start=1):
        require_keys(row, ["case_turn_id", "setting_short", "speaker", "text", "text_cn"])
        speaker = str(row["speaker"])

        predictor = patient_predictor if speaker in {"Patient", "Parent"} else pharmacist_predictor
        result = predictor(en_1=row["text"], cn_1=row["text_cn"])

        base = {
            "case_turn_id": row["case_turn_id"],
            "setting_short": row["setting_short"],
            "speaker": speaker,
            "en_1": row["text"],
            "cn_1": row["text_cn"],
        }
        generated = {field: getattr(result, field, None) for field in INSERTION_OUTPUT_FIELDS}
        output.append(base | generated)

        if idx % log_every == 0 or idx == len(rows):
            logger.info("error insertion progress: %s/%s", idx, len(rows))

    return output
