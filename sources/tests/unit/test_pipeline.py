"""Unit tests for the Phase 5 Pipeline Orchestration."""

import pytest
from pathlib import Path

from sources.core.manager import RepositoryManager
from sources.pipeline.pipeline_options import PipelineOptions
from sources.cache.validation_result import CacheValidationReason


@pytest.fixture
def test_workspace(tmp_path: Path) -> Path:
    """Setup a full valid test workspace with a config and module."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    # 1. Config
    config_file = workspace / "sources.yaml"
    odoo = workspace / "odoo"
    addons = odoo / "addons"

    config_file.write_text(
        "repositories:\n"
        "  framework:\n"
        "    '17.0':\n"
        f"      root: {odoo.resolve()}\n"
        f"      addons:\n"
        f"        - {addons.resolve()}\n"
    )

    # 2. Filesystem
    odoo = workspace / "odoo"
    odoo.mkdir()
    addons = odoo / "addons"
    addons.mkdir()

    mod = addons / "test_module"
    mod.mkdir()
    (mod / "__manifest__.py").write_text(
        "{\n    'name': 'Test',\n    'version': '1.0',\n    'depends': [],\n}\n"
    )

    return workspace


@pytest.fixture
def cache_db(tmp_path: Path) -> Path:
    return tmp_path / "cache.sqlite"


@pytest.fixture
def manager(cache_db: Path) -> RepositoryManager:
    return RepositoryManager(cache_db)


def test_pipeline_cache_miss_and_hit(test_workspace: Path, manager: RepositoryManager):
    """Test full pipeline execution: Miss -> Scan -> Store -> Hit."""
    config_path = test_workspace / "sources.yaml"

    # Run 1: Cache Miss
    result1 = manager.load(config_path)

    assert result1.success is True
    assert result1.context is not None
    assert result1.statistics.cache_miss is True
    assert result1.statistics.cache_hit is False
    assert result1.statistics.repositories_scanned == 1
    assert result1.statistics.modules_discovered == 1
    assert result1.cache_validation is None

    # Run 2: Cache Hit
    result2 = manager.load(config_path)

    assert result2.success is True
    assert result2.context is not None
    assert result2.statistics.cache_miss is False
    assert result2.statistics.cache_hit is True
    assert result2.statistics.repositories_scanned == 1
    assert result2.statistics.modules_loaded == 1
    assert result2.cache_validation is not None
    assert result2.cache_validation.reason == CacheValidationReason.CACHE_HIT


def test_pipeline_force_rescan(test_workspace: Path, manager: RepositoryManager):
    """Test force_rescan ignores cache."""
    config_path = test_workspace / "sources.yaml"

    manager.load(config_path)  # populate cache

    result = manager.scan(config_path)

    assert result.success is True
    assert result.statistics.cache_miss is True
    assert result.cache_validation is None


def test_pipeline_skip_cache(test_workspace: Path, manager: RepositoryManager):
    """Test skip_cache avoids saving and loading."""
    config_path = test_workspace / "sources.yaml"
    options = PipelineOptions(skip_cache=True)

    result = manager.load(config_path, options)
    assert result.success is True
    assert result.statistics.cache_miss is True


def test_pipeline_invalid_config(test_workspace: Path, manager: RepositoryManager):
    """Test pipeline gracefully handles config errors."""
    config_path = test_workspace / "sources.yaml"
    config_path.write_text("invalid_yaml: [")

    result = manager.load(config_path)

    assert result.success is False
    assert result.context is None
    assert len(result.errors) > 0


def test_pipeline_corrupted_cache_recovery(test_workspace: Path, manager: RepositoryManager):
    """Test pipeline handles a corrupted DB by doing a cache miss."""
    config_path = test_workspace / "sources.yaml"
    manager.load(config_path)  # populate cache

    # Corrupt the cache DB
    manager._cache_db_path.write_text("garbage")

    # Should catch the error, mark cache miss, and scan
    result = manager.load(config_path)

    assert result.success is True
    assert result.statistics.cache_miss is True
    assert len(result.warnings) > 0
    assert "Cache miss or load failure" in result.warnings[0]


def test_pipeline_configuration_changed(test_workspace: Path, manager: RepositoryManager):
    """Test changing config invalidates the cache."""
    config_path = test_workspace / "sources.yaml"
    manager.load(config_path)

    # Change config (change repo name)
    odoo = test_workspace / "odoo"
    config_path.write_text(
        f"repositories:\n  framework:\n    '17.0':\n      root: {odoo.resolve()}\n"
    )

    result = manager.load(config_path)

    assert result.success is True
    assert result.statistics.cache_miss is True
    assert result.cache_validation is not None
    assert result.cache_validation.reason == CacheValidationReason.CONFIGURATION_CHANGED
