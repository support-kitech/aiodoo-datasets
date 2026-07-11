"""Resolves and maps version dependencies across repositories."""

from collections import defaultdict
from types import MappingProxyType

from sources.domain.enums import OdooVersion
from sources.domain.repository import RepositoryConfiguration, ConfigurationSet
from sources.exceptions import ConfigurationError


class VersionResolver:
    """Resolves and validates version relationships between configurations."""

    @staticmethod
    def resolve_mappings(
        config_set: ConfigurationSet,
    ) -> MappingProxyType[OdooVersion, tuple[RepositoryConfiguration, ...]]:
        """
        Group configurations by version and ensure consistency.

        Args:
            config_set: The immutable ConfigurationSet.

        Returns:
            An immutable MappingProxyType mapping OdooVersion to its corresponding configurations.

        Raises:
            ConfigurationError: If conflicting configurations exist for a single version.
        """
        mapping: dict[OdooVersion, list[RepositoryConfiguration]] = defaultdict(list)

        for config in config_set.configurations:
            # Detect duplicate repository types for the same version
            existing_for_version = mapping[config.version]
            for existing in existing_for_version:
                if existing.repo_type == config.repo_type:
                    raise ConfigurationError(
                        f"Duplicate repository definition for type '{config.repo_type.value}' "
                        f"in version '{config.version.value}'."
                    )

            mapping[config.version].append(config)

        # Convert to immutable structures with deterministic ordering
        immutable_mapping: dict[OdooVersion, tuple[RepositoryConfiguration, ...]] = {}
        for version in sorted(mapping.keys(), key=lambda v: v.value):
            configs_for_version = mapping[version]
            configs_for_version.sort(key=lambda c: c.repo_type.value)
            immutable_mapping[version] = tuple(configs_for_version)

        return MappingProxyType(immutable_mapping)
