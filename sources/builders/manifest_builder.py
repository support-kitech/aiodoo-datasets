"""Assembles immutable RepositoryManifest objects."""

import hashlib

from sources.domain.repository import RepositoryConfiguration
from sources.domain.module import OdooModule
from sources.domain.manifest import RepositoryManifest, RepositoryFingerprint


class ManifestBuilder:
    """Builds RepositoryManifests from discovered modules and configuration."""

    @staticmethod
    def build(
        config: RepositoryConfiguration,
        modules: tuple[OdooModule, ...]
    ) -> RepositoryManifest:
        """
        Build the immutable manifest for the repository.

        Args:
            config: The repository configuration.
            modules: The tuple of fully instantiated OdooModules.

        Returns:
            An immutable RepositoryManifest object.
        """
        # 1. Deterministic hashing for modules
        module_hashes = []
        for mod in sorted(modules, key=lambda m: m.technical_name):
            mod_repr = f"{mod.technical_name}:{mod.version}:{','.join(mod.depends)}"
            module_hashes.append(mod_repr)
            
        manifest_hash_input = "|".join(module_hashes)
        manifest_hash = hashlib.sha256(manifest_hash_input.encode("utf-8")).hexdigest()

        # 2. Configuration hash
        addons_str = ",".join(str(p.resolve()) for p in sorted(config.addons_paths))
        config_repr = (
            f"{config.repository_name}:{config.repo_type.value}:"
            f"{config.version.value}:{str(config.root_path.resolve())}:"
            f"{addons_str}"
        )
        configuration_hash = hashlib.sha256(config_repr.encode("utf-8")).hexdigest()

        # 3. Overall Repository hash
        repo_hash_input = (
            f"{config.repository_name}:"
            f"{config.repo_type.value}:"
            f"{config.version.value}:"
            f"{manifest_hash_input}:"
            f"{config_repr}"
        )
        repository_hash = hashlib.sha256(repo_hash_input.encode("utf-8")).hexdigest()

        fingerprint = RepositoryFingerprint(
            configuration_hash=configuration_hash,
            manifest_hash=manifest_hash,
            repository_hash=repository_hash,
        )

        return RepositoryManifest(
            repository_name=config.repository_name,
            repository_type=config.repo_type,
            repository_version=config.version.value,
            module_count=len(modules),
            addons_count=len(config.addons_paths),
            fingerprint=fingerprint,
        )
