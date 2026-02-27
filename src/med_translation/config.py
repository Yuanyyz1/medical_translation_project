from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    input_dir: Path
    output_dir: Path
    openrouter_api_key: str
    default_model: str = "openrouter/openai/gpt-5-mini"
    qwen_model: str = "openrouter/qwen/qwen3-235b-a22b-2507"
    gemini_model: str = "openrouter/google/gemini-2.5-flash-lite"
    mistral_model: str = "openrouter/mistralai/devstral-2512"
    deepseek_model: str = "openrouter/deepseek/deepseek-v3.2"
    temperature: float = 1.0
    max_tokens: int = 16000

    @classmethod
    def load(cls, project_root: Path | None = None) -> "AppConfig":
        root = project_root or Path.cwd()
        load_dotenv(root / ".env")
        api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY is not set. Add it to your .env file."
            )

        input_dir = root / "inputs"
        output_dir = root / "outputs"
        output_dir.mkdir(parents=True, exist_ok=True)

        return cls(
            project_root=root,
            input_dir=input_dir,
            output_dir=output_dir,
            openrouter_api_key=api_key,
        )

    def with_runtime(self, temperature: float, max_tokens: int) -> "AppConfig":
        return AppConfig(
            project_root=self.project_root,
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            openrouter_api_key=self.openrouter_api_key,
            default_model=self.default_model,
            qwen_model=self.qwen_model,
            gemini_model=self.gemini_model,
            mistral_model=self.mistral_model,
            deepseek_model=self.deepseek_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
