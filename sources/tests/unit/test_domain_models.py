"""Unit tests for the Sources Framework domain models."""

from pathlib import Path
import pytest
from dataclasses import FrozenInstanceError

from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.module import OdooModule
from sources.domain.manifest import RepositoryFingerprint, RepositoryManifest
from sources.domain.repository import RepositoryConfiguration, Repository
from sources.domain.context import RepositoryContext


def test_odoo_module_immutability():
    """Test that OdooModule is immutable and has the expanded fields."""
    module = OdooModule(
        name="test_module",
        technical_name="test_module_tech",
        path=Path("/tmp/test_module"),
        manifest_path=Path("/tmp/test_module/__manifest__.py"),
        version="17.0",
        depends=("base",),
        license="LGPL-3",
        installable=True,
        application=False,
        auto_install=False,
    )
    assert module.name == "test_module"
    assert module.installable is True

    with pytest.raises(FrozenInstanceError):
        module.name = "new_name"  # type: ignore


def test_repository_fingerprint_immutability():
    """Test RepositoryFingerprint is immutable and uses deterministic hashes."""
    fingerprint = RepositoryFingerprint(
        configuration_hash="abc", manifest_hash="def", repository_hash="ghi"
    )
    assert fingerprint.configuration_hash == "abc"

    with pytest.raises(FrozenInstanceError):
        fingerprint.configuration_hash = "new_hash"  # type: ignore


def test_repository_manifest_immutability():
    """Test RepositoryManifest is immutable and uses the expanded fields."""
    fingerprint = RepositoryFingerprint(
        configuration_hash="abc", manifest_hash="def", repository_hash="ghi"
    )
    manifest = RepositoryManifest(
        repository_name="community",
        repository_type=RepositoryType.COMMUNITY,
        repository_version="17.0",
        module_count=5,
        addons_count=1,
        fingerprint=fingerprint,
    )

    assert manifest.module_count == 5
    with pytest.raises(FrozenInstanceError):
        manifest.module_count = 10  # type: ignore


def test_repository_configuration_immutability():
    """Test RepositoryConfiguration is immutable."""
    config = RepositoryConfiguration(
        repository_name="enterprise-17.0",
        repo_type=RepositoryType.ENTERPRISE,
        version=OdooVersion.V17,
        root_path=Path("/tmp/enterprise"),
        addons_paths=(Path("/tmp/enterprise/addons"),),
    )

    assert config.repo_type == RepositoryType.ENTERPRISE
    assert config.version == OdooVersion.V17
    with pytest.raises(FrozenInstanceError):
        config.root_path = Path("/tmp/other")  # type: ignore


def test_repository_properties_and_immutability():
    """Test Repository is immutable and exposes convenience properties correctly."""
    config = RepositoryConfiguration(
        repository_name="community-18.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V18,
        root_path=Path("/tmp/community"),
        addons_paths=(Path("/tmp/community/addons"),),
    )
    fingerprint = RepositoryFingerprint("abc", "def", "ghi")
    manifest = RepositoryManifest(
        repository_name="community",
        repository_type=RepositoryType.COMMUNITY,
        repository_version="18.0",
        module_count=1,
        addons_count=1,
        fingerprint=fingerprint,
    )
    module = OdooModule(
        name="base",
        technical_name="base",
        path=Path("/tmp/base"),
        manifest_path=Path("/tmp/base/__manifest__.py"),
        version="18.0",
        depends=(),
        license="LGPL-3",
        installable=True,
        application=True,
        auto_install=False,
    )

    repo = Repository(
        name="community",
        configuration=config,
        modules=(module,),
        manifest=manifest,
    )

    assert repo.name == "community"
    assert len(repo.modules) == 1
    # Test convenience properties
    assert repo.version == OdooVersion.V18
    assert repo.root_path == Path("/tmp/community")
    assert repo.repository_type == RepositoryType.COMMUNITY
    assert repo.addons_paths == (Path("/tmp/community/addons"),)

    with pytest.raises(FrozenInstanceError):
        repo.name = "new_name"  # type: ignore


def test_repository_context_immutability():
    """Test RepositoryContext is immutable and supports future expansion."""
    config = RepositoryConfiguration(
        repository_name="community-18.0",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V18,
        root_path=Path("/tmp/community"),
        addons_paths=(Path("/tmp/community/addons"),),
    )
    repo = Repository(
        name="community",
        configuration=config,
        modules=(),
        manifest=RepositoryManifest(
            repository_name="community",
            repository_type=RepositoryType.COMMUNITY,
            repository_version="18.0",
            module_count=0,
            addons_count=1,
            fingerprint=RepositoryFingerprint("a", "b", "c"),
        ),
    )

    context = RepositoryContext(
        repositories=(repo,),
        repository_index={"community_18.0": repo},
    )
    assert len(context.repositories) == 1
    assert context.repository_index["community_18.0"] == repo
    with pytest.raises(FrozenInstanceError):
        context.repositories = ()  # type: ignore
