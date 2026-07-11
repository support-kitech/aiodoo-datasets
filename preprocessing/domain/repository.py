"""Preprocessed Repository domain models for the Preprocessing Framework."""

from dataclasses import dataclass
from typing import Mapping
from types import MappingProxyType

from sources.domain.repository import OdooVersion, RepositoryType
from preprocessing.domain.file import NormalizedFile


@dataclass(frozen=True, slots=True)
class PreprocessedModule:
    """Immutable representation of a preprocessed Odoo module."""
    
    name: str
    files: tuple[NormalizedFile, ...]
    metadata: Mapping[str, object] = MappingProxyType({})


@dataclass(frozen=True, slots=True)
class PreprocessedRepository:
    """Immutable representation of a preprocessed repository."""
    
    name: str
    odoo_version: OdooVersion
    repository_type: RepositoryType
    modules: tuple[PreprocessedModule, ...]
    metadata: Mapping[str, object] = MappingProxyType({})
