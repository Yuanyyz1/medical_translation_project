from __future__ import annotations

from contextlib import contextmanager

import dspy

from .config import AppConfig


class ModelRegistry:
    def __init__(self, config: AppConfig):
        self.config = config
        self._models = {
            "default": self._make(config.default_model),
            "qwen": self._make(config.qwen_model),
            "gemini": self._make(config.gemini_model),
            "mistral": self._make(config.mistral_model),
            "deepseek": self._make(config.deepseek_model),
        }

    def _make(self, model_id: str) -> dspy.LM:
        return dspy.LM(
            model=model_id,
            api_key=self.config.openrouter_api_key,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

    def configure_default(self) -> None:
        lm = self._models["default"]
        dspy.settings.configure(lm=lm, track_usage=True)
        dspy.configure(lm=lm, track_usage=True)

    def get(self, model_name: str) -> dspy.LM:
        if model_name not in self._models:
            raise KeyError(f"Unknown model '{model_name}'. Available: {sorted(self._models)}")
        return self._models[model_name]

    @contextmanager
    def model_context(self, model_name: str):
        if model_name == "default":
            yield
            return
        with dspy.context(lm=self.get(model_name)):
            yield
