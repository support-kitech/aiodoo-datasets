"""Public API facade for the Sources Framework."""

from pathlib import Path

from sources.pipeline.pipeline import SourcesPipeline
from sources.pipeline.pipeline_options import PipelineOptions
from sources.pipeline.pipeline_result import PipelineResult


class RepositoryManager:
    """
    Public facade for the Sources Framework.
    Delegates entirely to SourcesPipeline. Contains zero business logic.
    """

    def __init__(self, cache_db_path: Path):
        self._pipeline = SourcesPipeline(cache_db_path)
        self._cache_db_path = cache_db_path

    def load(self, config_path: Path, options: PipelineOptions | None = None) -> PipelineResult:
        """
        Load the repository context using the provided configuration.
        
        Args:
            config_path: Path to the YAML configuration.
            options: Execution options (force_rescan, etc.)
            
        Returns:
            PipelineResult containing the full execution outcome.
        """
        if options is None:
            options = PipelineOptions()
        return self._pipeline.execute(config_path, options)

    def scan(self, config_path: Path) -> PipelineResult:
        """
        Force a fresh scan of the repositories, ignoring the cache.
        
        Args:
            config_path: Path to the YAML configuration.
            
        Returns:
            PipelineResult containing the full execution outcome.
        """
        options = PipelineOptions(force_rescan=True)
        return self._pipeline.execute(config_path, options)

    def refresh_cache(self, config_path: Path) -> PipelineResult:
        """
        Clear the existing cache and rebuild it from a fresh scan.
        
        Args:
            config_path: Path to the YAML configuration.
            
        Returns:
            PipelineResult containing the full execution outcome.
        """
        self.clear_cache()
        options = PipelineOptions(force_rescan=True)
        return self._pipeline.execute(config_path, options)

    def clear_cache(self) -> None:
        """Delete the cache database file."""
        if self._cache_db_path.exists():
            self._cache_db_path.unlink()
