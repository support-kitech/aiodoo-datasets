"""Loads and parses raw YAML configuration into immutable domain models."""

from pathlib import Path
from typing import Any

import yaml

from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.repository import RepositoryConfiguration, ConfigurationSet
from sources.exceptions import ConfigurationError


class RepositoryLoader:
    """Loads repository configuration from sources.yaml."""

    @staticmethod
    def load_sources(config_path: Path) -> ConfigurationSet:
        """
        Read and parse the sources YAML file into immutable configuration objects.

        Args:
            config_path: Path to sources.yaml.

        Returns:
            An immutable ConfigurationSet containing RepositoryConfiguration objects.

        Raises:
            ConfigurationError: If the file is missing, malformed, or invalid.
        """
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                raw_config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Malformed YAML in {config_path}: {e}")

        if not raw_config:
            raise ConfigurationError(f"Configuration file is empty: {config_path}")

        # Note: Validation is explicitly separated from loading.
        # The loader only converts valid YAML into Domain objects.
        # Assuming pipeline calls ConfigValidator beforehand.

        configurations: list[RepositoryConfiguration] = []
        repos: dict[str, Any] = raw_config.get("repositories", {})

        for repo_type_str, versions_config in repos.items():
            repo_type = RepositoryType(repo_type_str)

            for version_str, repo_details in versions_config.items():
                version = OdooVersion(version_str)
                root_path_str = repo_details["root"]
                
                # Automatically generate a stable repository name
                repository_name = f"{repo_type.value}-{version.value}"
                
                root_path = Path(root_path_str).resolve()
                
                addons_strs: list[str] = repo_details.get("addons", [])
                
                if addons_strs:
                    # Resolve relative to root_path
                    addons_paths = tuple((root_path / Path(p)).resolve() for p in addons_strs)
                else:
                    addons_paths = tuple()

                config = RepositoryConfiguration(
                    repository_name=repository_name,
                    repo_type=repo_type,
                    version=version,
                    root_path=root_path,
                    addons_paths=addons_paths,
                )
                configurations.append(config)

        # Enforce deterministic ordering (by name)
        configurations.sort(key=lambda c: c.repository_name)
        return ConfigurationSet(configurations=tuple(configurations))
