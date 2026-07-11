"""Unit tests for the RepositoryLoader and VersionResolver."""

import pytest
from pathlib import Path

from sources.core.loader import RepositoryLoader
from sources.core.version_resolver import VersionResolver
from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.repository import RepositoryConfiguration, ConfigurationSet
from sources.exceptions import ConfigurationError


def test_loader_missing_file(tmp_path: Path):
    """Test loader raises on missing file."""
    with pytest.raises(ConfigurationError, match="Configuration file not found"):
        RepositoryLoader.load_sources(tmp_path / "non_existent.yaml")


def test_loader_malformed_yaml(tmp_path: Path):
    """Test loader raises on invalid YAML."""
    config_file = tmp_path / "sources.yaml"
    config_file.write_text("invalid:\n- yaml:\n  - : error", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Malformed YAML"):
        RepositoryLoader.load_sources(config_file)


def test_loader_empty_yaml(tmp_path: Path):
    """Test loader raises on empty YAML."""
    config_file = tmp_path / "sources.yaml"
    config_file.write_text("", encoding="utf-8")

    with pytest.raises(ConfigurationError, match="Configuration file is empty"):
        RepositoryLoader.load_sources(config_file)


def test_loader_valid_configuration(tmp_path: Path):
    """Test loader parses a valid configuration into domain models."""
    config_file = tmp_path / "sources.yaml"
    config_file.write_text(
        "repositories:\n"
        "  community:\n"
        "    '17.0':\n"
        "      root: '/opt/odoo17'\n"
        "      addons:\n"
        "        - 'addons'\n"
        "  enterprise:\n"
        "    '17.0':\n"
        "      root: '/opt/enterprise17'\n",
        encoding="utf-8",
    )

    config_set = RepositoryLoader.load_sources(config_file)
    assert isinstance(config_set, ConfigurationSet)
    configs = config_set.configurations
    assert len(configs) == 2

    community = next(c for c in configs if c.repo_type == RepositoryType.COMMUNITY)
    assert community.repository_name == "community-17.0"
    assert community.version == OdooVersion.V17
    assert community.root_path == Path("/opt/odoo17").resolve()
    assert len(community.addons_paths) == 1
    assert community.addons_paths[0] == Path("/opt/odoo17/addons").resolve()

    enterprise = next(c for c in configs if c.repo_type == RepositoryType.ENTERPRISE)
    assert enterprise.repository_name == "enterprise-17.0"
    assert enterprise.version == OdooVersion.V17
    assert enterprise.root_path == Path("/opt/enterprise17").resolve()
    assert len(enterprise.addons_paths) == 0


def test_version_resolver_duplicate_repository():
    """Test VersionResolver catches duplicate repositories for the same version."""
    config1 = RepositoryConfiguration(
        repository_name="community-17.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V17,
        root_path=Path("/tmp/a"),
        addons_paths=(),
    )
    config2 = RepositoryConfiguration(
        repository_name="community-17.0-dup",
        repo_type=RepositoryType.COMMUNITY,  # Duplicate!
        version=OdooVersion.V17,
        root_path=Path("/tmp/b"),
        addons_paths=(),
    )

    config_set = ConfigurationSet(configurations=(config1, config2))
    with pytest.raises(ConfigurationError, match="Duplicate repository definition"):
        VersionResolver.resolve_mappings(config_set)


def test_version_resolver_valid_mappings():
    """Test VersionResolver successfully groups valid configurations."""
    c1 = RepositoryConfiguration(
        "community-17", RepositoryType.COMMUNITY, OdooVersion.V17, Path("a"), ()
    )
    c2 = RepositoryConfiguration(
        "enterprise-17", RepositoryType.ENTERPRISE, OdooVersion.V17, Path("b"), ()
    )
    c3 = RepositoryConfiguration(
        "community-18", RepositoryType.COMMUNITY, OdooVersion.V18, Path("c"), ()
    )

    config_set = ConfigurationSet(configurations=(c1, c2, c3))
    mapping = VersionResolver.resolve_mappings(config_set)

    assert len(mapping) == 2
    assert OdooVersion.V17 in mapping
    assert len(mapping[OdooVersion.V17]) == 2
    assert OdooVersion.V18 in mapping
    assert len(mapping[OdooVersion.V18]) == 1
