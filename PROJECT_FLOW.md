# Medical Translation Project Flow

## Purpose
This document explains how the project runs end-to-end based on the current code paths, including:
- Two-script workflow: `scripts/run_insert_errors.py` then `scripts/run_detect_errors.py`
- Unified CLI workflow: `python -m med_translation.cli run-all`

Expected primary inputs:
- `inputs/original_conversations.xlsx`
- `.env` with `OPENROUTER_API_KEY`

Major outputs:
- `outputs/original_conversations_errors.xlsx` (insertion/intermediate output)
- `outputs/final_detection*.xlsx` (final detection output, single- or multi-model)

## ASCII Flowchart (Numbered Steps)
```text
START
  |
  v
[HIGH-LEVEL NOTE 1: SETTING]
[S0] Runtime setup context
     - Python environment and dependencies ready
     - .env available with OPENROUTER_API_KEY
     - Input/output paths chosen
  |
  v
[S1] Load config + API key
     AppConfig.load() -> require OPENROUTER_API_KEY
  |
  v
[S2] Initialize model registry
     ModelRegistry(cfg), configure_default()
  |
  v
[S3] Read input Excel
     read_excel_records(input_path)
  |
  v
[S4] Optional row selection
     --row-index OR --rows OR --row-start/--row-end
     (scripts/insert supports all 3; detect and run-all use row-index)
  |
  v
[HIGH-LEVEL NOTE 2: ERROR INSERTIONS]
[S5] Filter short rows (insertion path)
     keep rows where word_count(text) > 5
  |
  v
[S6] Run error insertion
     run_error_insertion()
     speaker route: Patient/Parent -> patient predictor
                    others -> pharmacist predictor
  |
  v
[S7] Write insertion output
     write_excel_records(..., intermediate_path)
  |
  v
[HIGH-LEVEL NOTE 3: ERROR DETECTION]
[S8] Build detection inputs from insertion rows
     build_detection_inputs()
  |
  v
[S9] Run detection per model
     run_detection_for_models()
       -> loop models
       -> run_error_detection() inside model context
  |
  v
[S10] Merge model outputs
      merge_detection_results()
      add model suffixes: _<model_name>
  |
  v
[S11] Write final detection output
      write_dataframe(..., output_path)
  |
  v
END
```

## Step-by-step Table
| Step | What it does | Input | Output | Where in code |
|---|---|---|---|---|
| S1 | Loads runtime config and validates API key from `.env`. | Working directory, `.env` (`OPENROUTER_API_KEY`) | `AppConfig` object with model IDs, temperature, max tokens, paths | `src/med_translation/config.py` (`AppConfig.load`, `with_runtime`) |
| S2 | Builds LM registry and sets default DSPy LM context. | `AppConfig` | `ModelRegistry` with models (`default`, `qwen`, `gemini`, `mistral`, `deepseek`) | `src/med_translation/models.py` (`ModelRegistry`, `configure_default`, `model_context`) |
| S3 | Reads source Excel into row dictionaries. | Input `.xlsx` path | `list[dict]` records | `src/med_translation/io.py` (`read_excel_records`) |
| S4 | Applies optional row subset selection and validates selector rules/ranges. | `rows` + selector args | Selected rows | `src/med_translation/cli.py` (`select_rows`) |
| S5 | Filters out short source utterances before insertion. | Selected rows with `text` | Rows where `word_count(text) > 5` | `src/med_translation/pipelines/error_insertion.py` (`filter_long_rows`) |
| S6 | Generates translation-error variants for each row; checks required insertion keys and routes by speaker. | Required insertion keys: `case_turn_id`, `setting_short`, `speaker`, `text`, `text_cn` | Inserted rows containing base fields (`en_1`, `cn_1`, etc.) + insertion outputs (`errors_1..3`, `errors_domain_1..3`, `errors_explain_1..3`, `en_2_1..3`, `cn_2_1..3`, `error_best`, `error_best_explain`, `ambiguity`) | `src/med_translation/pipelines/error_insertion.py` (`run_error_insertion`) |
| S7 | Writes insertion/intermediate dataset to Excel. | Inserted rows | Intermediate `.xlsx` (commonly `outputs/original_conversations_errors.xlsx`) | `src/med_translation/io.py` (`write_excel_records`) |
| S8 | Shapes insertion rows into fixed detection input schema and validates required fields. | Insertion rows with detection-required columns | Detection rows with fields: `case_turn_id`, `setting_short`, `speaker`, `en_1`, `cn_2_1`, `cn_1`, `en_2_1`, `errors_1`, `errors_domain_1`, `errors_explain_1` | `src/med_translation/pipelines/error_detection.py` (`build_detection_inputs`, `DETECTION_INPUT_FIELDS`) |
| S9 | Runs error detection for one or more models; each model executes predictor on each row and extracts detection outputs. | Detection rows + `--models` list + `ModelRegistry` | `dict[model_name -> list[dict]]` with detection fields | `src/med_translation/pipelines/error_detection.py` (`run_detection_for_models`, `run_error_detection`) |
| S10 | Validates and merges per-model detection outputs into one table; appends model suffixes. | Base detection rows + per-model results | `DataFrame` with columns like `errors_detected_text1_<model>`, `errors_detected_domain_text1_<model>`, `errors_detected_domain_explain_text1_<model>`, `clinical_consequences_explain_text1_<model>`, `clinical_consequences_flag_text1_<model>`, same for text2, plus `ambiguity_<model>` | `src/med_translation/pipelines/merge.py` (`merge_detection_results`) |
| S11 | Writes merged final detection table to Excel. | Merged `DataFrame` | Final `.xlsx` (for example `outputs/final_detection.xlsx`, `outputs/final_detection_multi_models.xlsx`) | `src/med_translation/io.py` (`write_dataframe`) |

## Execution Paths
- Script path (two commands):
  1. `python scripts/run_insert_errors.py ...` runs S1-S7
  2. `python scripts/run_detect_errors.py ...` runs S1-S4 (row-index option), then S8-S11
- CLI path (single command):
  - `python -m med_translation.cli run-all ...` runs S1-S11 in one command and writes the intermediate insertion file before detection.

## Failure Points / Validations
- Missing API key:
  - `AppConfig.load()` raises if `OPENROUTER_API_KEY` is absent or empty.
- Missing input file:
  - `read_excel_records()` raises `FileNotFoundError` for non-existent input path.
- Invalid row selectors:
  - `select_rows()` raises for mutually exclusive selector use, out-of-range indices, invalid ranges, or incomplete range args.
- Missing required detection columns for merge:
  - `merge_detection_results()` raises if a model output is missing required detection fields before suffixing/concatenation.
