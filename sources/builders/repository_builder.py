"""Assembles immutable Repository objects."""

from sources.domain.repository import RepositoryConfiguration, Repository
from sources.domain.module import OdooModule
from sources.builders.manifest_builder import ManifestBuilder


class RepositoryBuilder:
    """Assembles full Repository objects."""

    @staticmethod
    def build(config: RepositoryConfiguration, modules: tuple[OdooModule, ...]) -> Repository:
        """
        Build the immutable Repository object.

        Args:
            config: The valid repository configuration.
            modules: The tuple of discovered and instantiated modules.

        Returns:
            An immutable Repository instance.
        """
        # Ensure modules are deterministically ordered
        sorted_modules = tuple(sorted(modules, key=lambda m: m.technical_name))

        # Build the manifest
        manifest = ManifestBuilder.build(config, sorted_modules)

        # Assemble the repository
        return Repository(
            name=config.repository_name,
            configuration=config,
            modules=sorted_modules,
            manifest=manifest,
        )
