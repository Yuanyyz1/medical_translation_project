from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _bootstrap_path() -> None:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run error detection only.")
    parser.add_argument(
        "--input",
        default="outputs/original_conversations_errors.xlsx",
        help="Path to insertion result xlsx.",
    )
    parser.add_argument(
        "--output",
        default="outputs/final_detection.xlsx",
        help="Path to output detection xlsx.",
    )
    parser.add_argument(
        "--models",
        default="default",
        help="Comma-separated models, e.g. default,qwen,gemini.",
    )
    parser.add_argument(
        "--row-index",
        type=int,
        default=None,
        help="Optional zero-based row index to run a single row only.",
    )
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--max-tokens", type=int, default=16000)
    parser.add_argument("--log-level", default="INFO")
    return parser


def main() -> None:
    _bootstrap_path()
    from med_translation.cli import command_detect_errors
    from med_translation.logging_utils import configure_logging

    parser = build_parser()
    args = parser.parse_args()
    configure_logging(args.log_level)
    command_detect_errors(args)
    print(f"Saved detection output: {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
