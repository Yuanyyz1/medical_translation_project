# Daily Use Guide

This file is a personal quick guide for day-to-day runs.

## One-time setup (not every day)

Run this only when first setting up, or after dependency updates:

```powershell
python -m pip install -r requirements.txt
```

## Each time you open VS Code

1. Open a new terminal in project root.
   Project root means this folder:
   `C:\Users\gao0372\OneDrive - Flinders\Project materials\6. LLM translation\codes\medical_translation_project`
   If terminal opens elsewhere, run:

```powershell
cd "C:\Users\gao0372\OneDrive - Flinders\Project materials\6. LLM translation\codes\medical_translation_project"
```

2. Enable script running for this terminal session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

3. Activate virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Confirm you see `(.venv)` in terminal prompt.

## Common commands

### Insert errors (first row only)

```powershell
python scripts/run_insert_errors.py --row-index 0 --output outputs/original_conversations_errors_toy.xlsx
```

### Insert errors (full dataset)

```powershell
python scripts/run_insert_errors.py --input inputs/original_conversations.xlsx --output outputs/original_conversations_errors.xlsx
```

### Insert errors (selected rows)

```powershell
python scripts/run_insert_errors.py --rows 0,3,5 --output outputs/original_conversations_errors_subset.xlsx
python scripts/run_insert_errors.py --row-start 10 --row-end 20 --output outputs/original_conversations_errors_range.xlsx
```

### Detect errors (first row, default model)

```powershell
python scripts/run_detect_errors.py --row-index 0 --models default --input outputs/original_conversations_errors_toy.xlsx --output outputs/final_detection_toy.xlsx
```

### Detect errors (full dataset, default model)

```powershell
python scripts/run_detect_errors.py --models default --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_default.xlsx
```

### Detect errors (all models)

```powershell
python scripts/run_detect_errors.py --models default,qwen,gemini,mistral,deepseek --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_multi_models.xlsx
```

## Model Selection (Detection)

Use `--models` to choose which model(s) run in detection.

Available model names:
- `default`
- `qwen`
- `gemini`
- `mistral`
- `deepseek`

`default` currently maps to: `openrouter/openai/gpt-5-mini`.

Single model example:

```powershell
python scripts/run_detect_errors.py --models gemini --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_gemini.xlsx
```

Multiple models example:

```powershell
python scripts/run_detect_errors.py --models default,qwen,gemini,deepseek --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_multi_models.xlsx
```

If `mistral` fails with a model availability error, run without `mistral` or update the model slug in `src/med_translation/config.py`.

### How to add a new model

1. Open `src/med_translation/config.py`.
2. Add a new model field in `AppConfig`, for example:
   `my_new_model: str = "openrouter/<provider>/<model-slug>"`
3. Open `src/med_translation/models.py`.
4. Register it in `ModelRegistry._models`, for example:
   `"mynew": self._make(config.my_new_model),`
5. Run detection using the new short name:

```powershell
python scripts/run_detect_errors.py --models mynew --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_mynew.xlsx
```

6. Optional: include it in multi-model runs:
   `--models default,qwen,gemini,mynew`

### End-to-end (full run in two commands)

```powershell
python scripts/run_insert_errors.py --input inputs/original_conversations.xlsx --output outputs/original_conversations_errors.xlsx
python scripts/run_detect_errors.py --models default,qwen,gemini,mistral,deepseek --input outputs/original_conversations_errors.xlsx --output outputs/final_detection_multi_models.xlsx
```

## Useful row options (insertion script)

- Single row: `--row-index 0`
- Multiple rows: `--rows 0,3,5`
- Range: `--row-start 10 --row-end 20`

## If key issue happens

If you changed `.env` key but terminal still uses old one:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 7) What not in this file

Advanced tasks (for example, adding new models) are not in this daily guide.

Use `README.md` for project internals and advanced configuration.
