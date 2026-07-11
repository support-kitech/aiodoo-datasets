"""Unit tests for the ConfigValidator and RepositoryValidator."""

import pytest
from pathlib import Path

from sources.validation.config_validator import ConfigValidator
from sources.validation.repository_validator import RepositoryValidator
from sources.domain.repository import RepositoryConfiguration
from sources.domain.enums import RepositoryType, OdooVersion
from sources.exceptions import ConfigurationError, ValidationError


def test_config_validator_missing_repositories():
    """Test validation fails if 'repositories' key is missing."""
    with pytest.raises(ConfigurationError, match="Missing 'repositories' key"):
        ConfigValidator.validate_sources_yaml({"other": {}})


def test_config_validator_invalid_repository_type():
    """Test validation fails for unsupported repository types."""
    config = {"repositories": {"unknown_type": {}}}
    with pytest.raises(ConfigurationError, match="Invalid repository type 'unknown_type'"):
        ConfigValidator.validate_sources_yaml(config)


def test_config_validator_unsupported_version():
    """Test validation fails for unsupported Odoo versions."""
    config = {
        "repositories": {
            "community": {
                "15.0": {"root": "/tmp"}
            }
        }
    }
    with pytest.raises(ConfigurationError, match="Unsupported Odoo version '15.0'"):
        ConfigValidator.validate_sources_yaml(config)


def test_config_validator_missing_root():
    """Test validation fails if 'root' is missing."""
    config = {
        "repositories": {
            "community": {
                "17.0": {"addons": ["a"]}
            }
        }
    }
    with pytest.raises(ConfigurationError, match="Missing 'root' path"):
        ConfigValidator.validate_sources_yaml(config)


def test_repository_validator_missing_root(tmp_path: Path):
    """Test validation fails if physical root path does not exist."""
    config = RepositoryConfiguration(
        repository_name="community-17.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V17,
        root_path=tmp_path / "does_not_exist",
        addons_paths=(),
    )
    with pytest.raises(ValidationError, match="Repository root path does not exist"):
        RepositoryValidator.validate_configuration(config)


def test_repository_validator_missing_addon(tmp_path: Path):
    """Test validation fails if a physical addon path does not exist."""
    root = tmp_path / "odoo"
    root.mkdir()
    
    config = RepositoryConfiguration(
        repository_name="community-17.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V17,
        root_path=root,
        addons_paths=(root / "missing_addon",),
    )
    with pytest.raises(ValidationError, match="Addon path does not exist"):
        RepositoryValidator.validate_configuration(config)


def test_repository_validator_duplicate_addon_paths(tmp_path: Path):
    """Test validation fails if addon paths resolve to the same location."""
    root = tmp_path / "odoo"
    root.mkdir()
    addon = root / "addons"
    addon.mkdir()
    
    # Intentionally duplicate addon path
    config = RepositoryConfiguration(
        repository_name="community-17.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V17,
        root_path=root,
        addons_paths=(addon, addon),
    )
    
    with pytest.raises(ValidationError, match="Duplicate addon path detected"):
        RepositoryValidator.validate_configuration(config)


def test_repository_validator_valid_paths(tmp_path: Path):
    """Test validation succeeds when paths exist and are unique."""
    root = tmp_path / "odoo"
    root.mkdir()
    addon1 = root / "addons1"
    addon1.mkdir()
    addon2 = root / "addons2"
    addon2.mkdir()
    
    config = RepositoryConfiguration(
        repository_name="community-17.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V17,
        root_path=root,
        addons_paths=(addon1, addon2),
    )
    
    # Should not raise any exceptions
    RepositoryValidator.validate_configuration(config)
