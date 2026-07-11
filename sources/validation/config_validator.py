"""Validates raw configuration dictionaries before instantiation."""

from typing import Any, Mapping

from sources.domain.enums import RepositoryType, OdooVersion
from sources.exceptions import ConfigurationError


class ConfigValidator:
    """Validates raw configuration parsed from YAML files."""

    @staticmethod
    def validate_sources_yaml(config: Mapping[str, Any]) -> None:
        """
        Validate the basic structure of the raw sources.yaml.

        Args:
            config: Raw parsed YAML dictionary.

        Raises:
            ConfigurationError: If the structure is invalid.
        """
        if not isinstance(config, dict):
            raise ConfigurationError("Configuration must be a dictionary.")

        if "repositories" not in config:
            raise ConfigurationError("Missing 'repositories' key in configuration.")

        repos = config["repositories"]
        if not isinstance(repos, dict):
            raise ConfigurationError("'repositories' must be a dictionary.")

        for repo_type_str, versions_config in repos.items():
            # Validate RepositoryType
            try:
                RepositoryType(repo_type_str)
            except ValueError:
                valid_types = [t.value for t in RepositoryType]
                raise ConfigurationError(
                    f"Invalid repository type '{repo_type_str}'. "
                    f"Must be one of {valid_types}."
                )

            if not isinstance(versions_config, dict):
                raise ConfigurationError(
                    f"Configuration for '{repo_type_str}' must be a dictionary of versions."
                )

            for version_str, repo_details in versions_config.items():
                # Validate Version
                try:
                    OdooVersion(version_str)
                except ValueError:
                    valid_versions = [v.value for v in OdooVersion]
                    raise ConfigurationError(
                        f"Unsupported Odoo version '{version_str}' in '{repo_type_str}'. "
                        f"Must be one of {valid_versions}."
                    )

                if not isinstance(repo_details, dict):
                    raise ConfigurationError(
                        f"Details for '{repo_type_str}' version '{version_str}' must be a dictionary."
                    )

                if "root" not in repo_details:
                    raise ConfigurationError(
                        f"Missing 'root' path for '{repo_type_str}' version '{version_str}'."
                    )

                if not isinstance(repo_details["root"], str):
                    raise ConfigurationError(
                        f"'root' path for '{repo_type_str}' version '{version_str}' must be a string."
                    )
                
                if "addons" in repo_details:
                    if not isinstance(repo_details["addons"], list):
                        raise ConfigurationError(
                            f"'addons' for '{repo_type_str}' version '{version_str}' must be a list of strings."
                        )
                    for addon_path in repo_details["addons"]:
                        if not isinstance(addon_path, str):
                            raise ConfigurationError(
                                f"'addons' paths for '{repo_type_str}' version '{version_str}' must be strings."
                            )
