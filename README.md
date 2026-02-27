# Medical Translation Pipeline (Refactored)

This project refactors notebook logic into reusable Python modules while keeping the original notebook unchanged:
- `Medical_translation_openrouter_dspy_updated.local.ipynb`

## Project Structure

```text
.
├─ src/med_translation/
│  ├─ cli.py
│  ├─ config.py
│  ├─ io.py
│  ├─ logging_utils.py
│  ├─ models.py
│  ├─ prompts.py
│  ├─ signatures.py
│  ├─ types.py
│  ├─ utils.py
│  └─ pipelines/
│     ├─ error_insertion.py
│     ├─ error_detection.py
│     └─ merge.py
├─ tests/
├─ notebooks/
├─ inputs/
└─ outputs/
```

## Setup

```bash
python -m pip install -r requirements.txt
```

PowerShell (once per terminal session):

```powershell
$env:PYTHONPATH = "src"
```

Set `.env`:

```env
OPENROUTER_API_KEY=your_key_here
```

## Main Entry Point

```bash
python -m med_translation.cli
```

## Commands

1. Run insertion only
```bash
python -m med_translation.cli insert-errors --input inputs/original_conversations.xlsx --output outputs/original_conversations_errors.xlsx
```

2. Run detection only
```bash
python -m med_translation.cli detect-errors --input outputs/original_conversations_errors.xlsx --output outputs/final_detection.xlsx --models default,qwen,gemini,mistral,deepseek
```

3. Run full pipeline
```bash
python -m med_translation.cli run-all --input inputs/original_conversations.xlsx --intermediate outputs/original_conversations_errors.xlsx --output outputs/final_detection.xlsx --models default,qwen,gemini,mistral,deepseek
```

4. Run a single row (toy example, row 0)
```bash
python -m med_translation.cli run-all --input inputs/original_conversations.xlsx --intermediate outputs/original_conversations_errors_toy.xlsx --output outputs/final_detection_toy.xlsx --models default --row-index 0
```

`--row-index` is zero-based. Example: `0` means first row, `1` means second row.

## Standalone Scripts

You can also run insertion and detection as separate scripts:

1. Insertion only (`scripts/run_insert_errors.py`)
```bash
python scripts/run_insert_errors.py --row-index 0
```

2. Detection only (`scripts/run_detect_errors.py`)
```bash
python scripts/run_detect_errors.py --row-index 0 --models default
```

Run detection with multiple models:
```bash
python scripts/run_detect_errors.py --models default,qwen,gemini,mistral,deepseek --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_multi_models.xlsx
```

Common options for both scripts:
- `--input`: input xlsx path
- `--output`: output xlsx path
- `--row-index`: run a single row (zero-based)
- `--temperature`: model temperature
- `--max-tokens`: model max tokens
- `--log-level`: logging level (e.g., `INFO`, `DEBUG`)

Additional row options for insertion script (`scripts/run_insert_errors.py`):
- `--rows`: comma-separated zero-based indexes (example: `--rows 0,3,5`)
- `--row-start` and `--row-end`: index range (start inclusive, end exclusive)

Examples:
```bash
python scripts/run_insert_errors.py --rows 0,3,5 --output outputs/original_conversations_errors_subset.xlsx
python scripts/run_insert_errors.py --row-start 10 --row-end 20 --output outputs/original_conversations_errors_range.xlsx
```

Example with custom paths:
```bash
python scripts/run_insert_errors.py --input inputs/original_conversations.xlsx --output outputs/original_conversations_errors_toy.xlsx --row-index 0
python scripts/run_detect_errors.py --input outputs/original_conversations_errors_toy.xlsx --output outputs/final_detection_toy.xlsx --models default --row-index 0
```

### Detection Output Structure

Detection output includes:
- Base input columns (for example: `case_turn_id`, `setting_short`, `speaker`, `en_1`, `cn_2_1`, `cn_1`, `en_2_1`, `errors_1`, `errors_domain_1`, `errors_explain_1`)
- One set of model-specific columns per model, suffixed by model name:
  - `_default`
  - `_qwen`
  - `_gemini`
  - `_mistral`
  - `_deepseek`

Each model contributes these fields (with suffix):
- `errors_detected_text1_*`
- `errors_detected_domain_text1_*`
- `errors_detected_domain_explain_text1_*`
- `clinical_consequences_explain_text1_*`
- `clinical_consequences_flag_text1_*`
- `errors_detected_text2_*`
- `errors_detected_domain_text2_*`
- `errors_detected_domain_explain_text2_*`
- `clinical_consequences_explain_text2_*`
- `clinical_consequences_flag_text2_*`
- `ambiguity_*`

## Extending the Project

### Add a New Model
1. Add the model id to `AppConfig` in `src/med_translation/config.py`.
2. Register it in `ModelRegistry` in `src/med_translation/models.py`.
3. Include it in CLI `--models`.

### Change Prompts
1. Update prompt constants in `src/med_translation/prompts.py`.
2. Keep field names aligned with signatures in `src/med_translation/signatures.py`.
3. Add or update tests if output schema changes.

### Adapt Input Dataset
1. Ensure required input columns exist (`case_turn_id`, `setting_short`, `speaker`, `text`, `text_cn`).
2. Update mapping and validation in `src/med_translation/pipelines/error_insertion.py`.
3. Add tests for new schema in `tests/`.

### Customize Outputs
1. Update detection output column list in `src/med_translation/pipelines/error_detection.py`.
2. Update merge behavior in `src/med_translation/pipelines/merge.py`.
3. Keep suffixing by model name for multi-model comparisons.

## Testing

### Run all tests
```bash
pytest -q
```

### Run one file
```bash
pytest tests/test_merge.py -q
```

### Run one test
```bash
pytest tests/test_merge.py::test_merge_detection_results_success -q
```

### Useful options
```bash
pytest -vv
pytest -x
pytest --lf
```

## What Tests Tell You

- `tests/test_utils.py`: utility behavior is stable.
- `tests/test_merge.py`: merge schema and explicit column handling are stable.
- `tests/test_pipeline_wiring.py`: speaker and prediction wiring work with mocked outputs.

If a test fails, the failure usually points to the exact module or function where behavior changed.
