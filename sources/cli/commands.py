"""Command implementations mapping CLI args to RepositoryManager."""

import json
import sys
from pathlib import Path
from dataclasses import asdict

from sources.core.manager import RepositoryManager
from sources.pipeline.pipeline_options import PipelineOptions
from sources.pipeline.pipeline_result import PipelineResult


class CliCommands:
    """Handles execution of specific CLI commands."""

    def __init__(self, manager: RepositoryManager, config_path: Path, as_json: bool):
        self.manager = manager
        self.config_path = config_path
        self.as_json = as_json

    def _output(self, result: PipelineResult, data_dict: dict) -> None:
        """Helper to print output conditionally as JSON or human readable."""
        if self.as_json:
            print(json.dumps(data_dict, indent=2))
        else:
            if result.success:
                print("✓ Success")
            else:
                print("✗ Failed")

            if result.errors:
                print("\nErrors:")
                for e in result.errors:
                    print(f"  - {e}")
            if result.warnings:
                print("\nWarnings:")
                for w in result.warnings:
                    print(f"  - {w}")

            print("\nStatistics:")
            stats_dict = asdict(result.statistics)
            for k, v in stats_dict.items():
                if isinstance(v, float):
                    print(f"  {k.replace('_', ' ').title()}: {v:.3f} sec")
                else:
                    print(f"  {k.replace('_', ' ').title()}: {v}")

        sys.exit(0 if result.success else 1)

    def scan(self, options: PipelineOptions) -> None:
        """Scan command: Forces rescan and loads."""
        # scan command implies force_rescan=True
        scan_options = PipelineOptions(
            force_rescan=True, skip_cache=options.skip_cache, validate_only=options.validate_only
        )
        result = self.manager.load(self.config_path, scan_options)

        data = {
            "success": result.success,
            "errors": result.errors,
            "warnings": result.warnings,
            "statistics": asdict(result.statistics),
        }

        self._output(result, data)

    def validate(self, options: PipelineOptions) -> None:
        """Validate command: Just loads with validate_only flag."""
        val_options = PipelineOptions(
            force_rescan=options.force_rescan, skip_cache=options.skip_cache, validate_only=True
        )
        result = self.manager.load(self.config_path, val_options)

        data = {
            "success": result.success,
            "errors": result.errors,
            "warnings": result.warnings,
            "statistics": asdict(result.statistics),
        }

        self._output(result, data)

    def summary(self, options: PipelineOptions) -> None:
        """Summary command: Loads and prints high-level summary of the framework state."""
        result = self.manager.load(self.config_path, options)

        if not result.success or not result.context:
            self._output(result, {"success": False, "errors": result.errors})
            return

        context = result.context
        repo_count = len(context.repositories)
        module_count = sum(len(r.modules) for r in context.repositories)
        versions = list({r.version.value for r in context.repositories})
        types = list({r.repository_type.value for r in context.repositories})

        data = {
            "success": True,
            "summary": {
                "repositories": repo_count,
                "modules": module_count,
                "versions": sorted(versions),
                "types": sorted(types),
            },
            "statistics": asdict(result.statistics),
        }

        if self.as_json:
            print(json.dumps(data, indent=2))
        else:
            print("=== Sources Framework Summary ===")
            print(f"Repositories: {repo_count}")
            print(f"Modules: {module_count}")
            print(f"Versions: {', '.join(sorted(versions))}")
            print(f"Types: {', '.join(sorted(types))}")
            print("=================================")
            print("\nCache Statistics:")
            print(f"  Hit: {result.statistics.cache_hit}")
            print(f"  Miss: {result.statistics.cache_miss}")
            print(f"  Total Time: {result.statistics.total_duration:.3f} sec")

        sys.exit(0)

    def cache_info(self, options: PipelineOptions) -> None:
        """Display information about the cache."""
        result = self.manager.load(self.config_path, options)

        if not result.success:
            self._output(result, {"success": False, "errors": result.errors})
            return

        db_path = self.manager._cache_db_path
        size = db_path.stat().st_size if db_path.exists() else 0

        val_reason = result.cache_validation.reason.value if result.cache_validation else "NONE"
        val_msg = ""

        data = {
            "success": True,
            "cache_state": {
                "exists": db_path.exists(),
                "size_bytes": size,
                "hit": result.statistics.cache_hit,
                "validation_reason": val_reason,
                "validation_message": val_msg,
            },
        }

        if self.as_json:
            print(json.dumps(data, indent=2))
        else:
            print("=== Cache Information ===")
            print(f"Database: {db_path}")
            print(f"Size: {size / 1024 / 1024:.2f} MB")
            print(f"Hit Status: {'HIT' if result.statistics.cache_hit else 'MISS'}")
            print(f"Validation Reason: {val_reason}")
            if val_msg:
                print(f"Validation Message: {val_msg}")

        sys.exit(0)

    def cache_clear(self, options: PipelineOptions) -> None:
        """Clear the cache."""
        self.manager.clear_cache()
        data = {"success": True, "message": "Cache cleared."}
        if self.as_json:
            print(json.dumps(data, indent=2))
        else:
            print("✓ Cache successfully cleared.")
        sys.exit(0)

    def refresh_cache(self, options: PipelineOptions) -> None:
        """Clear and refresh the cache."""
        result = self.manager.refresh_cache(self.config_path)
        data = {
            "success": result.success,
            "errors": result.errors,
            "warnings": result.warnings,
            "statistics": asdict(result.statistics),
        }
        if self.as_json:
            print(json.dumps(data, indent=2))
        else:
            print(
                "✓ Cache successfully refreshed." if result.success else "✗ Cache refresh failed."
            )
            print(f"Repositories Scanned: {result.statistics.repositories_scanned}")
            print(f"Modules Discovered: {result.statistics.modules_discovered}")
            print(f"Duration: {result.statistics.total_duration:.3f} sec")

        sys.exit(0 if result.success else 1)
