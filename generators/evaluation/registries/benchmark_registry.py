"""Benchmark Registry for Evaluation Generator."""

from typing import Dict, Any
from types import MappingProxyType


class BenchmarkRegistry:
    """Static registry for benchmark suites."""

    _benchmarks: Dict[str, Any] = {}
    _frozen: bool = False

    @classmethod
    def register(cls, suite_name: str, suite_definition: Any) -> None:
        """Register a benchmark suite statically."""
        if cls._frozen:
            raise RuntimeError("BenchmarkRegistry is frozen and cannot be modified.")
        cls._benchmarks[suite_name] = suite_definition

    @classmethod
    def get(cls, suite_name: str) -> Any:
        """Retrieve a benchmark suite by name."""
        return cls._benchmarks.get(suite_name)

    @classmethod
    def freeze(cls) -> None:
        """Freeze the registry to prevent further modification."""
        cls._frozen = True

    @classmethod
    def get_all(cls) -> MappingProxyType:
        """Return a read-only mapping of all registered benchmarks."""
        return MappingProxyType(cls._benchmarks)
