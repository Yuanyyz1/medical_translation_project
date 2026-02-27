from types import SimpleNamespace

from med_translation.pipelines.error_detection import (
    DETECTION_OUTPUT_FIELDS,
    build_detection_inputs,
    run_error_detection,
)
from med_translation.pipelines.error_insertion import run_error_insertion


class FakeInsertPredictor:
    def __init__(self, tag: str):
        self.tag = tag

    def __call__(self, **kwargs):
        payload = {
            "errors_1": f"e1_{self.tag}",
            "errors_domain_1": "domain",
            "errors_explain_1": "explain",
            "en_2_1": "en2",
            "cn_2_1": "cn2",
            "errors_2": "e2",
            "errors_domain_2": "domain",
            "errors_explain_2": "explain",
            "en_2_2": "en2",
            "cn_2_2": "cn2",
            "errors_3": "e3",
            "errors_domain_3": "domain",
            "errors_explain_3": "explain",
            "en_2_3": "en2",
            "cn_2_3": "cn2",
            "error_best": "best",
            "error_best_explain": "best_explain",
            "ambiguity": "",
        }
        return SimpleNamespace(**payload)


class FakeDetectPredictor:
    def __call__(self, **kwargs):
        return SimpleNamespace(**{field: f"out_{field}" for field in DETECTION_OUTPUT_FIELDS})


def test_insertion_routes_by_speaker():
    rows = [
        {
            "case_turn_id": "1",
            "setting_short": "A",
            "speaker": "Pharmacist",
            "text": "one two three four five six",
            "text_cn": "cn",
        },
        {
            "case_turn_id": "2",
            "setting_short": "A",
            "speaker": "Patient",
            "text": "one two three four five six",
            "text_cn": "cn",
        },
    ]

    results = run_error_insertion(
        rows,
        pharmacist_predictor=FakeInsertPredictor("pharmacist"),
        patient_predictor=FakeInsertPredictor("patient"),
        log_every=100,
    )

    assert results[0]["errors_1"] == "e1_pharmacist"
    assert results[1]["errors_1"] == "e1_patient"


def test_detection_pipeline_wiring():
    insertion_rows = [
        {
            "case_turn_id": "1",
            "setting_short": "A",
            "speaker": "Pharmacist",
            "en_1": "source",
            "cn_2_1": "translated",
            "cn_1": "source2",
            "en_2_1": "translated2",
            "errors_1": "Negation",
            "errors_domain_1": "domain",
            "errors_explain_1": "explain",
        }
    ]

    detection_input = build_detection_inputs(insertion_rows)
    outputs = run_error_detection(detection_input, predictor=FakeDetectPredictor(), log_every=100)

    assert outputs[0]["errors_detected_text1"] == "out_errors_detected_text1"
