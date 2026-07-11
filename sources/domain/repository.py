"""Domain models for Repositories and their configurations."""

from dataclasses import dataclass
from pathlib import Path

from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.manifest import RepositoryManifest
from sources.domain.module import OdooModule


@dataclass(frozen=True, slots=True)
class RepositoryConfiguration:
    """Immutable configuration dictating where and how to scan a repository."""

    repository_name: str
    repo_type: RepositoryType
    version: OdooVersion
    root_path: Path
    addons_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class ConfigurationSet:
    """Immutable collection of parsed repository configurations."""

    configurations: tuple[RepositoryConfiguration, ...]


@dataclass(frozen=True, slots=True)
class Repository:
    """Immutable representation of a fully loaded Odoo repository."""

    name: str
    configuration: RepositoryConfiguration
    modules: tuple[OdooModule, ...]
    manifest: RepositoryManifest

    @property
    def version(self) -> OdooVersion:
        """Convenience property to access the repository version."""
        return self.configuration.version

    @property
    def root_path(self) -> Path:
        """Convenience property to access the repository root path."""
        return self.configuration.root_path

    @property
    def repository_type(self) -> RepositoryType:
        """Convenience property to access the repository type."""
        return self.configuration.repo_type

    @property
    def addons_paths(self) -> tuple[Path, ...]:
        """Convenience property to access the repository addon paths."""
        return self.configuration.addons_paths
