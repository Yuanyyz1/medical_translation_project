from __future__ import annotations

import argparse
from pathlib import Path

from .config import AppConfig
from .io import read_excel_records, write_dataframe, write_excel_records
from .logging_utils import configure_logging
from .pipelines.error_detection import build_detection_inputs, run_detection_for_models
from .pipelines.error_insertion import filter_long_rows, run_error_insertion
from .pipelines.merge import merge_detection_results


def parse_models(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(",") if part.strip()]


def select_rows(
    rows: list[dict],
    row_index: int | None = None,
    rows_csv: str | None = None,
    row_start: int | None = None,
    row_end: int | None = None,
) -> list[dict]:
    selectors = [
        row_index is not None,
        bool(rows_csv),
        row_start is not None or row_end is not None,
    ]
    if sum(selectors) > 1:
        raise ValueError("Use only one of --row-index, --rows, or --row-start/--row-end.")

    if row_index is not None:
        if row_index < 0 or row_index >= len(rows):
            raise ValueError(
                f"--row-index {row_index} is out of range for dataset of size {len(rows)}"
            )
        return [rows[row_index]]

    if rows_csv:
        indexes: list[int] = []
        for token in rows_csv.split(","):
            token = token.strip()
            if not token:
                continue
            idx = int(token)
            if idx < 0 or idx >= len(rows):
                raise ValueError(f"Row index {idx} in --rows is out of range for dataset size {len(rows)}")
            indexes.append(idx)
        if not indexes:
            raise ValueError("--rows was provided but no valid row indexes were found.")
        return [rows[idx] for idx in indexes]

    if row_start is not None or row_end is not None:
        if row_start is None or row_end is None:
            raise ValueError("Provide both --row-start and --row-end together.")
        if row_start < 0 or row_end < 0:
            raise ValueError("--row-start and --row-end must be >= 0.")
        if row_start >= row_end:
            raise ValueError("--row-start must be less than --row-end.")
        if row_end > len(rows):
            raise ValueError(f"--row-end {row_end} is out of range for dataset size {len(rows)}")
        return rows[row_start:row_end]

    return rows


def command_insert_errors(args: argparse.Namespace) -> None:
    from .models import ModelRegistry

    cfg = AppConfig.load().with_runtime(args.temperature, args.max_tokens)
    registry = ModelRegistry(cfg)
    registry.configure_default()

    rows = read_excel_records(Path(args.input))
    rows = select_rows(
        rows,
        row_index=getattr(args, "row_index", None),
        rows_csv=getattr(args, "rows", None),
        row_start=getattr(args, "row_start", None),
        row_end=getattr(args, "row_end", None),
    )
    filtered = filter_long_rows(rows)
    generated = run_error_insertion(filtered)
    write_excel_records(generated, Path(args.output))


def command_detect_errors(args: argparse.Namespace) -> None:
    from .models import ModelRegistry

    cfg = AppConfig.load().with_runtime(args.temperature, args.max_tokens)
    registry = ModelRegistry(cfg)
    registry.configure_default()

    insertion_rows = read_excel_records(Path(args.input))
    insertion_rows = select_rows(insertion_rows, args.row_index)
    detection_input = build_detection_inputs(insertion_rows)
    model_names = parse_models(args.models)
    detection_by_model = run_detection_for_models(detection_input, model_names, registry)
    merged = merge_detection_results(detection_input, detection_by_model)
    write_dataframe(merged, Path(args.output))


def command_run_all(args: argparse.Namespace) -> None:
    from .models import ModelRegistry

    cfg = AppConfig.load().with_runtime(args.temperature, args.max_tokens)
    registry = ModelRegistry(cfg)
    registry.configure_default()

    rows = read_excel_records(Path(args.input))
    rows = select_rows(rows, args.row_index)
    filtered = filter_long_rows(rows)
    inserted = run_error_insertion(filtered)
    write_excel_records(inserted, Path(args.intermediate))

    detection_input = build_detection_inputs(inserted)
    model_names = parse_models(args.models)
    detection_by_model = run_detection_for_models(detection_input, model_names, registry)
    merged = merge_detection_results(detection_input, detection_by_model)
    write_dataframe(merged, Path(args.output))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Medical translation pipeline CLI")
    parser.add_argument("--log-level", default="INFO")
    subparsers = parser.add_subparsers(dest="command", required=True)

    insert_parser = subparsers.add_parser("insert-errors", help="Generate translation errors")
    insert_parser.add_argument("--input", required=True)
    insert_parser.add_argument("--output", required=True)
    insert_parser.add_argument("--temperature", type=float, default=1.0)
    insert_parser.add_argument("--max-tokens", type=int, default=16000)
    insert_parser.add_argument(
        "--row-index",
        type=int,
        default=None,
        help="Run only one row by zero-based index from the input dataset.",
    )
    insert_parser.set_defaults(func=command_insert_errors)

    detect_parser = subparsers.add_parser("detect-errors", help="Run error detection")
    detect_parser.add_argument("--input", required=True)
    detect_parser.add_argument("--output", required=True)
    detect_parser.add_argument("--models", default="default,qwen,gemini,mistral,deepseek")
    detect_parser.add_argument("--temperature", type=float, default=1.0)
    detect_parser.add_argument("--max-tokens", type=int, default=16000)
    detect_parser.add_argument(
        "--row-index",
        type=int,
        default=None,
        help="Run only one row by zero-based index from the input dataset.",
    )
    detect_parser.set_defaults(func=command_detect_errors)

    run_all = subparsers.add_parser("run-all", help="Run insertion and detection")
    run_all.add_argument("--input", required=True)
    run_all.add_argument("--intermediate", required=True)
    run_all.add_argument("--output", required=True)
    run_all.add_argument("--models", default="default,qwen,gemini,mistral,deepseek")
    run_all.add_argument("--temperature", type=float, default=1.0)
    run_all.add_argument("--max-tokens", type=int, default=16000)
    run_all.add_argument(
        "--row-index",
        type=int,
        default=None,
        help="Run only one row by zero-based index from the input dataset.",
    )
    run_all.set_defaults(func=command_run_all)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    configure_logging(args.log_level)
    args.func(args)


if __name__ == "__main__":
    main()
