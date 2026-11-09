"""Loads backend/config/model_config.yaml (the single place model names live)."""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Optional

import yaml
from pydantic import BaseModel, Field, model_validator

from app.config import CONFIG_DIR


class ModelSpec(BaseModel):
    id: str                                # exact NEAR AI model id sent to the API
    input_per_m: float                     # USD per 1M input tokens
    output_per_m: float                    # USD per 1M output tokens
    cache_read_per_m: Optional[float] = None
    context_length: Optional[int] = None
    structured_outputs: bool = False       # advertised by the catalogue
    json_mode: bool = False
    reasoning: bool = False


class AgentModelConfig(BaseModel):
    primary: str
    fallbacks: list[str] = Field(default_factory=list)
    temperature: float = 0.2
    max_tokens: int = 4096
    timeout_s: float = 120.0
    # sent only to models with reasoning: true. "low" stopped DeepSeek V4.1 Flash from spending its
    # whole output budget on hidden reasoning (live, 2026-11-08). Dropped automatically if a model rejects it.
    reasoning_effort: Optional[Literal["low", "medium", "high"]] = None


class ModelConfig(BaseModel):
    prices_verified_on: str = ""
    prices_source: str = ""
    models: dict[str, ModelSpec]
    agents: dict[str, AgentModelConfig]

    @model_validator(mode="after")
    def _aliases_exist(self) -> "ModelConfig":
        for agent, cfg in self.agents.items():
            for alias in [cfg.primary, *cfg.fallbacks]:
                if alias not in self.models:
                    raise ValueError(f"agent '{agent}' uses unknown model alias '{alias}'")
        return self


def load_model_config(path: Optional[Path] = None) -> ModelConfig:
    path = path or (CONFIG_DIR / "model_config.yaml")
    with open(path, "r", encoding="utf-8") as fh:
        return ModelConfig.model_validate(yaml.safe_load(fh))
