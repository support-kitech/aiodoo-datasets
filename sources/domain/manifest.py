"""Domain models for repository manifests and fingerprints."""

from dataclasses import dataclass

from sources.domain.enums import RepositoryType


@dataclass(frozen=True, slots=True)
class RepositoryFingerprint:
    """Deterministic hashes representing the repository state."""

    configuration_hash: str
    manifest_hash: str
    repository_hash: str


@dataclass(frozen=True, slots=True)
class RepositoryManifest:
    """Metadata about the scanned repository."""

    repository_name: str
    repository_type: RepositoryType
    repository_version: str
    module_count: int
    addons_count: int
    fingerprint: RepositoryFingerprint
