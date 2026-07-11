"""Domain model for the pipeline RepositoryContext."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from sources.domain.repository import Repository


@dataclass(frozen=True, slots=True)
class RepositoryContext:
    """Immutable context containing all loaded and validated repositories."""

    repositories: tuple[Repository, ...]
    repository_index: Mapping[str, Repository] = field(default_factory=lambda: MappingProxyType({}))
    configuration: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    statistics: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
