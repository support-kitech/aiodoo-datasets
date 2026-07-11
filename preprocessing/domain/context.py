"""Context domain models for the Preprocessing Framework."""

from dataclasses import dataclass
from typing import Mapping
from types import MappingProxyType

from preprocessing.domain.repository import PreprocessedRepository


@dataclass(frozen=True, slots=True)
class PreprocessedRepositoryContext:
    """
    Immutable representation of all repositories after preprocessing.
    This is the ultimate output of the Preprocessing Framework.
    """

    repositories: tuple[PreprocessedRepository, ...]
    metadata: Mapping[str, object] = MappingProxyType({})
