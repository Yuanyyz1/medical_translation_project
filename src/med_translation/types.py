from __future__ import annotations

from typing import TypedDict


class ConversationRow(TypedDict, total=False):
    case_turn_id: str
    setting_short: str
    speaker: str
    text: str
    text_cn: str


class ErrorInsertionRow(TypedDict, total=False):
    case_turn_id: str
    setting_short: str
    speaker: str
    en_1: str
    cn_1: str
    errors_1: str
    errors_domain_1: str
    errors_explain_1: str
    en_2_1: str
    cn_2_1: str
    errors_2: str
    errors_domain_2: str
    errors_explain_2: str
    en_2_2: str
    cn_2_2: str
    errors_3: str
    errors_domain_3: str
    errors_explain_3: str
    en_2_3: str
    cn_2_3: str
    error_best: str
    error_best_explain: str
    ambiguity: str


class DetectionRow(TypedDict, total=False):
    case_turn_id: str
    setting_short: str
    speaker: str
    en_1: str
    cn_2_1: str
    cn_1: str
    en_2_1: str
    errors_1: str
    errors_domain_1: str
    errors_explain_1: str
