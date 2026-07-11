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

    def __getstate__(self):
        return (self.name, self.files, dict(self.metadata))

    def __setstate__(self, state):
        name, files, metadata_dict = state
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "files", files)
        object.__setattr__(self, "metadata", MappingProxyType(metadata_dict))


@dataclass(frozen=True, slots=True)
class PreprocessedRepository:
    """Immutable representation of a preprocessed repository."""

    name: str
    odoo_version: OdooVersion
    repository_type: RepositoryType
    modules: tuple[PreprocessedModule, ...]
    metadata: Mapping[str, object] = MappingProxyType({})

    def __getstate__(self):
        return (
            self.name,
            self.odoo_version,
            self.repository_type,
            self.modules,
            dict(self.metadata),
        )

    def __setstate__(self, state):
        name, odoo_version, repository_type, modules, metadata_dict = state
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "odoo_version", odoo_version)
        object.__setattr__(self, "repository_type", repository_type)
        object.__setattr__(self, "modules", modules)
        object.__setattr__(self, "metadata", MappingProxyType(metadata_dict))
