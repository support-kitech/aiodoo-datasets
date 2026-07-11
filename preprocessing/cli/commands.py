"""CLI Commands implementation for the Preprocessing Framework."""

import json
from pathlib import Path

from preprocessing.core.manager import PreprocessingManager
from preprocessing.cli.arguments import CliArgs, to_pipeline_options
from preprocessing.exceptions import PreprocessingError
from sources.core.manager import RepositoryManager
from sources.domain.context import RepositoryContext


class CommandHandler:
    """Handles CLI command execution, mapping CLI logic to Manager facade."""
    
    def __init__(self, manager: PreprocessingManager, args: CliArgs):
        self.manager = manager
        self.args = args
        
    def _get_source_context(self) -> RepositoryContext:
        """Fetch the RepositoryContext from the Sources Framework."""
        if not self.args.config:
            # Fallback to default if not provided, assuming typical usage in aiodoo-datasets
            config_path = Path("config/sources.yaml")
        else:
            config_path = Path(self.args.config)
            
        if not config_path.exists():
            raise PreprocessingError(f"Configuration file not found: {config_path}")
            
        repo_manager = RepositoryManager(Path("config/sources.sqlite"))
        from sources.pipeline.pipeline_options import PipelineOptions
        result = repo_manager.load(config_path, PipelineOptions())
        if not result.success or not result.context:
            raise PreprocessingError("Failed to load sources context.")
        return result.context

    def execute(self) -> int:
        """Execute the command and return a POSIX exit code."""
        if self.args.command == "normalize":
            return self.normalize()
        elif self.args.command == "validate":
            return self.validate()
        elif self.args.command == "summary":
            return self.summary()
        elif self.args.command == "cache-info":
            return self.cache_info()
        elif self.args.command == "cache-clear":
            return self.cache_clear()
        elif self.args.command == "refresh-cache":
            return self.refresh_cache()
        elif self.args.command == "benchmark":
            return self.benchmark()
        return 4
        
    def normalize(self) -> int:
        ctx = self._get_source_context()
        options = to_pipeline_options(self.args)
        result = self.manager.normalize(ctx, options)
        
        if not result.success:
            if self.args.json_output:
                print(json.dumps({"error": result.error_message}))
            else:
                print(f"Normalization failed: {result.error_message}")
            return 4
            
        if self.args.json_output:
            out = {
                "success": True,
                "repositories_processed": result.statistics.repositories_processed,
                "files_processed": result.statistics.files_processed,
                "total_duration": result.statistics.total_duration,
                "cache_hit": result.statistics.cache_hit
            }
            print(json.dumps(out))
        else:
            print("✓ Repository Loaded")
            print(f"✓ Cache Hit: {result.statistics.cache_hit}")
            print(f"✓ Files Processed: {result.statistics.files_processed}")
            print(f"✓ Processing Time: {result.statistics.total_duration:.2f} sec")
            
        return 0

    def validate(self) -> int:
        ctx = self._get_source_context()
        result = self.manager.validate(ctx)
        
        if not result.success:
            if self.args.json_output:
                print(json.dumps({"valid": False, "error": result.error_message}))
            else:
                print(f"Validation failed: {result.error_message}")
            return 1
            
        if self.args.json_output:
            print(json.dumps({"valid": True, "validation_time": result.statistics.validation_time}))
        else:
            print("✓ Validation passed successfully.")
            
        return 0

    def summary(self) -> int:
        # Same as normalize but outputting detailed stats
        ctx = self._get_source_context()
        options = to_pipeline_options(self.args)
        result = self.manager.normalize(ctx, options)
        if not result.success:
            return 4
            
        if self.args.json_output:
            print(json.dumps({"stats": result.statistics.__dict__}))
        else:
            print("--- Preprocessing Summary ---")
            print(f"Repositories: {result.statistics.repositories_processed}")
            print(f"Files: {result.statistics.files_processed}")
            print(f"Cache Hit: {result.statistics.cache_hit}")
            print(f"Total Duration: {result.statistics.total_duration:.2f}s")
        return 0

    def cache_info(self) -> int:
        # In a real app we'd query sqlite DB for the schema directly
        from preprocessing.constants.framework import PREPROCESSING_FRAMEWORK_VERSION, CACHE_SCHEMA_VERSION
        
        out = {
            "framework_version": PREPROCESSING_FRAMEWORK_VERSION,
            "cache_schema_version": CACHE_SCHEMA_VERSION,
        }
        
        if self.args.json_output:
            print(json.dumps(out))
        else:
            print(f"Framework Version: {PREPROCESSING_FRAMEWORK_VERSION}")
            print(f"Cache Schema Version: {CACHE_SCHEMA_VERSION}")
            
        return 0

    def cache_clear(self) -> int:
        self.manager.clear_cache()
        if self.args.json_output:
            print(json.dumps({"cleared": True}))
        else:
            print("✓ Cache cleared.")
        return 0

    def refresh_cache(self) -> int:
        ctx = self._get_source_context()
        result = self.manager.refresh_cache(ctx)
        if not result.success:
            return 4
        if self.args.json_output:
            print(json.dumps({"refreshed": True}))
        else:
            print("✓ Cache refreshed successfully.")
        return 0

    def benchmark(self) -> int:
        import subprocess
        # Simply proxy to the benchmark script
        subprocess.run(["python", "-m", "preprocessing.cli.scripts.benchmark"])
        return 0
