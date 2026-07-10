"""Runtime configuration."""

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RuntimeConfig:
    """Immutable configuration for pipeline runtime behavior."""
    debug_mode: bool = False
    fail_fast: bool = True
    log_level: str = "INFO"
