import pytest

from med_translation.pipelines.error_detection import DETECTION_OUTPUT_FIELDS
from med_translation.pipelines.merge import merge_detection_results


def make_detection_row():
    return {field: f"value_{field}" for field in DETECTION_OUTPUT_FIELDS}


def test_merge_detection_results_success():
    base = [{"case_turn_id": "1", "en_1": "hello"}]
    detection = {"default": [make_detection_row()], "qwen": [make_detection_row()]}

    merged = merge_detection_results(base, detection)

    assert "errors_detected_text1_default" in merged.columns
    assert "errors_detected_text1_qwen" in merged.columns
    assert len(merged) == 1


def test_merge_detection_results_missing_columns_raises():
    base = [{"case_turn_id": "1"}]
    detection = {"default": [{"errors_detected_text1": "x"}]}

    with pytest.raises(ValueError):
        merge_detection_results(base, detection)
