"""Generator configuration."""

from dataclasses import dataclass
from typing import Any
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class GeneratorConfig:
    """Immutable configuration for the generators."""

    version: str = "1.0.0"
    max_parallel_phases: int = 4
    allow_cycles: bool = False
    strict_validation: bool = True
    custom_settings: MappingProxyType[str, Any] = MappingProxyType({})
