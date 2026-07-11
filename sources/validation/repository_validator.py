"""Validates RepositoryConfiguration objects before scanning."""

from sources.domain.repository import RepositoryConfiguration
from sources.exceptions import ValidationError


class RepositoryValidator:
    """Validates physical constraints and logical integrity of configurations."""

    @staticmethod
    def validate_configuration(config: RepositoryConfiguration) -> None:
        """
        Ensure the physical paths in the configuration actually exist.

        Args:
            config: The immutable configuration object.

        Raises:
            ValidationFailedError: If paths do not exist or are invalid.
        """
        if not config.root_path.exists():
            raise ValidationError(
                f"Repository root path does not exist for {config.repo_type.value} "
                f"({config.version.value}): {config.root_path}"
            )

        if not config.root_path.is_dir():
            raise ValidationError(
                f"Repository root path is not a directory for {config.repo_type.value} "
                f"({config.version.value}): {config.root_path}"
            )

        # Ensure no duplicate addon paths exist in the same config
        seen_addons: set[str] = set()

        for addon_path in config.addons_paths:
            if not addon_path.exists():
                raise ValidationError(
                    f"Addon path does not exist for {config.repo_type.value} "
                    f"({config.version.value}): {addon_path}"
                )
            
            if not addon_path.is_dir():
                raise ValidationError(
                    f"Addon path is not a directory for {config.repo_type.value} "
                    f"({config.version.value}): {addon_path}"
                )
                
            resolved_str = str(addon_path.resolve())
            if resolved_str in seen_addons:
                raise ValidationError(
                    f"Duplicate addon path detected in {config.repo_type.value} "
                    f"({config.version.value}): {addon_path}"
                )
            seen_addons.add(resolved_str)
