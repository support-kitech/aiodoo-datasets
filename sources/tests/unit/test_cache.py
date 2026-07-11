"""Unit tests for the Phase 4 Cache Framework."""

import pytest
import time
from pathlib import Path

from sources.domain.enums import RepositoryType, OdooVersion
from sources.domain.repository import RepositoryConfiguration, Repository
from sources.domain.module import OdooModule
from sources.domain.manifest import RepositoryManifest, RepositoryFingerprint
from sources.domain.context import RepositoryContext

from sources.cache.cache_key import CacheKey
from sources.cache.cache_metadata import CacheMetadata
from sources.cache.store import CacheStore
from sources.cache.invalidator import CacheInvalidator
from sources.cache.validation_result import CacheValidationReason
from sources.constants.framework import SOURCES_FRAMEWORK_VERSION
from sources.constants.cache import CACHE_SCHEMA_VERSION
from sources.exceptions import CacheError


@pytest.fixture
def sample_repository_context(tmp_path: Path) -> RepositoryContext:
    """Fixture to provide a full immutable RepositoryContext."""
    config = RepositoryConfiguration(
        repository_name="test-repo",
        repo_type=RepositoryType.COMMUNITY,
        version=OdooVersion.V17,
        root_path=tmp_path / "odoo",
        addons_paths=(tmp_path / "odoo" / "addons",),
    )
    
    module = OdooModule(
        name="Test Module",
        technical_name="test_module",
        path=tmp_path / "odoo" / "addons" / "test_module",
        manifest_path=tmp_path / "odoo" / "addons" / "test_module" / "__manifest__.py",
        version="1.0",
        depends=(),
        license="LGPL-3",
        installable=True,
        application=False,
        auto_install=False,
    )
    
    fingerprint = RepositoryFingerprint(
        configuration_hash="conf_hash",
        manifest_hash="man_hash",
        repository_hash="repo_hash",
    )
    
    manifest = RepositoryManifest(
        repository_name="test-repo",
        repository_type=RepositoryType.COMMUNITY,
        repository_version="17.0",
        module_count=1,
        addons_count=1,
        fingerprint=fingerprint,
    )
    
    repo = Repository(
        name="test-repo",
        configuration=config,
        modules=(module,),
        manifest=manifest,
    )
    
    return RepositoryContext(repositories=(repo,))


@pytest.fixture
def cache_store(tmp_path: Path) -> CacheStore:
    """Fixture providing a CacheStore instance."""
    return CacheStore(tmp_path / ".cache" / "sources.sqlite")


def test_cache_store_save_load(cache_store: CacheStore, sample_repository_context: RepositoryContext):
    """Test saving and loading RepositoryContext from the SQLite cache."""
    metadata = CacheMetadata(
        cache_schema_version=CACHE_SCHEMA_VERSION,
        sources_framework_version=SOURCES_FRAMEWORK_VERSION,
        python_version="3.12.0",
        repository_count=1,
        module_count=1,
        configuration_hash="conf_hash",
        repository_hash="repo_hash",
        creation_time=time.time(),
        last_validation=time.time(),
    )
    
    # Save cache
    cache_store.save(sample_repository_context, metadata)
    assert cache_store.db_path.exists()
    
    # Load cache
    loaded_context, loaded_metadata = cache_store.load()
    
    assert loaded_metadata.cache_schema_version == CACHE_SCHEMA_VERSION
    assert loaded_metadata.sources_framework_version == SOURCES_FRAMEWORK_VERSION
    
    assert len(loaded_context.repositories) == 1
    repo = loaded_context.repositories[0]
    
    assert repo.name == "test-repo"
    assert repo.version == OdooVersion.V17
    assert len(repo.modules) == 1
    assert repo.modules[0].technical_name == "test_module"
    
    # The store rebuilds the RepositoryIndex dynamically
    assert "test-repo" in loaded_context.repository_index


def test_cache_store_clear(cache_store: CacheStore, sample_repository_context: RepositoryContext):
    """Test clearing the cache deletes the SQLite DB."""
    metadata = CacheMetadata(
        cache_schema_version=CACHE_SCHEMA_VERSION,
        sources_framework_version=SOURCES_FRAMEWORK_VERSION,
        python_version="3.12.0",
        repository_count=1,
        module_count=1,
        configuration_hash="conf_hash",
        repository_hash="repo_hash",
        creation_time=time.time(),
        last_validation=time.time(),
    )
    
    cache_store.save(sample_repository_context, metadata)
    assert cache_store.db_path.exists()
    
    cache_store.clear()
    assert not cache_store.db_path.exists()
    
    # Loading cleared cache should raise CacheError
    with pytest.raises(CacheError, match="Cache database does not exist"):
        cache_store.load()


def test_cache_invalidator_valid():
    """Test CacheInvalidator returns True for matching keys."""
    python_ver = CacheInvalidator.get_python_version()
    key = CacheKey(
        repository_name="all",
        configuration_hash="conf123",
        repository_hash="repo123",
        framework_version=SOURCES_FRAMEWORK_VERSION,
        python_version=python_ver,
        cache_schema_version=CACHE_SCHEMA_VERSION,
    )
    
    metadata = CacheMetadata(
        sources_framework_version=SOURCES_FRAMEWORK_VERSION,
        cache_schema_version=CACHE_SCHEMA_VERSION,
        python_version=python_ver,
        repository_count=1,
        module_count=1,
        configuration_hash="conf123",
        repository_hash="repo123",
        creation_time=time.time(),
        last_validation=time.time(),
    )
    
    result = CacheInvalidator.validate(key, metadata)
    assert result.is_valid is True
    assert result.reason == CacheValidationReason.CACHE_HIT


def test_cache_invalidator_invalid_schema():
    """Test CacheInvalidator returns False when schema version changes."""
    key = CacheKey(
        repository_name="all",
        configuration_hash="conf123",
        repository_hash="repo123",
        framework_version=SOURCES_FRAMEWORK_VERSION,
        python_version=CacheInvalidator.get_python_version(),
        cache_schema_version="2.0",
    )
    
    metadata = CacheMetadata(
        sources_framework_version=SOURCES_FRAMEWORK_VERSION,
        cache_schema_version="1.0",
        python_version=CacheInvalidator.get_python_version(),
        repository_count=1,
        module_count=1,
        configuration_hash="conf123",
        repository_hash="repo123",
        creation_time=time.time(),
        last_validation=time.time(),
    )
    
    result = CacheInvalidator.validate(key, metadata)
    assert result.is_valid is False
    assert result.reason == CacheValidationReason.SCHEMA_CHANGED


def test_cache_invalidator_invalid_fingerprint():
    """Test CacheInvalidator returns False when hashes change."""
    python_ver = CacheInvalidator.get_python_version()
    key = CacheKey(
        repository_name="all",
        configuration_hash="conf999",  # Changed!
        repository_hash="repo123",
        framework_version=SOURCES_FRAMEWORK_VERSION,
        python_version=python_ver,
        cache_schema_version=CACHE_SCHEMA_VERSION,
    )
    
    metadata = CacheMetadata(
        sources_framework_version=SOURCES_FRAMEWORK_VERSION,
        cache_schema_version=CACHE_SCHEMA_VERSION,
        python_version=python_ver,
        repository_count=1,
        module_count=1,
        configuration_hash="conf123",
        repository_hash="repo123",
        creation_time=time.time(),
        last_validation=time.time(),
    )
    
    result = CacheInvalidator.validate(key, metadata)
    assert result.is_valid is False
    assert result.reason == CacheValidationReason.CONFIGURATION_CHANGED
