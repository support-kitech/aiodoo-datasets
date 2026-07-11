"""Unit tests for Phase 3 Cache & Orchestration."""

import unittest
from pathlib import Path
import tempfile

from preprocessing.core.manager import PreprocessingManager
from preprocessing.pipeline.pipeline_options import PipelineOptions
from sources.domain.context import RepositoryContext
from sources.domain.repository import Repository, RepositoryConfiguration
from sources.domain.module import OdooModule
from sources.domain.enums import OdooVersion, RepositoryType


class TestPhase3(unittest.TestCase):
    """Test Cache, Serializer, and Pipeline Orchestration."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "cache.sqlite"
        self.manager = PreprocessingManager(self.db_path)

        # Create a mock source context
        # We need a real file to trigger pipeline reading
        self.test_file = Path(self.temp_dir.name) / "test.py"
        self.test_file.write_text("def test():\n    pass")

        module = OdooModule(
            name="test_module",
            technical_name="test_module",
            path=Path(self.temp_dir.name),
            manifest_path=Path(self.temp_dir.name) / "__manifest__.py",
            version="1.0",
            depends=tuple(),
            license="LGPL-3",
            installable=True,
            application=False,
            auto_install=False,
        )

        repo_config = RepositoryConfiguration(
            repository_name="test_repo",
            repo_type=RepositoryType.ENTERPRISE,
            version=OdooVersion.V17,
            root_path=Path(self.temp_dir.name),
            addons_paths=tuple(),
        )

        from sources.domain.manifest import RepositoryManifest, RepositoryFingerprint

        fingerprint = RepositoryFingerprint(
            configuration_hash="a", manifest_hash="b", repository_hash="c"
        )
        manifest = RepositoryManifest(
            repository_name="test_repo",
            repository_type=RepositoryType.ENTERPRISE,
            repository_version="17.0",
            module_count=1,
            addons_count=0,
            fingerprint=fingerprint,
        )

        repo = Repository(
            name="test_repo", configuration=repo_config, modules=(module,), manifest=manifest
        )

        self.source_context = RepositoryContext(repositories=(repo,))
        # Mocking hash property dynamically or since we don't have it natively, let's inject it.
        # Wait, RepositoryContext doesn't have .hash. I need to monkey patch it for the test.
        # Or let's see how I implemented cache key fallback.

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_pipeline_cache_hit_miss(self):
        # 1. Miss (First run)
        result1 = self.manager.normalize(self.source_context)
        self.assertTrue(result1.success)
        self.assertTrue(result1.statistics.cache_miss)
        self.assertFalse(result1.statistics.cache_hit)

        # 2. Hit (Second run)
        result2 = self.manager.normalize(self.source_context)
        self.assertTrue(result2.success)
        self.assertFalse(result2.statistics.cache_miss)
        self.assertTrue(result2.statistics.cache_hit)

        # 3. Force Reprocess
        options = PipelineOptions(force_reprocess=True)
        result3 = self.manager.normalize(self.source_context, options=options)
        self.assertTrue(result3.success)
        self.assertTrue(result3.statistics.cache_miss)
        self.assertFalse(result3.statistics.cache_hit)


if __name__ == "__main__":
    unittest.main()
