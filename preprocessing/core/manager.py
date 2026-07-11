"""PreprocessingManager public facade."""

from pathlib import Path

from sources.domain.context import RepositoryContext
from preprocessing.pipeline.pipeline import PreprocessingPipeline
from preprocessing.pipeline.pipeline_context import PipelineContext
from preprocessing.pipeline.pipeline_options import PipelineOptions
from preprocessing.pipeline.pipeline_result import PipelineResult
from preprocessing.cache.store import CacheStore
from preprocessing.processors.registry import ProcessorRegistry
from preprocessing.processors.text.whitespace import WhitespaceProcessor
from preprocessing.processors.text.line_ending import LineEndingProcessor
from preprocessing.processors.syntax.python import PythonProcessor
from preprocessing.processors.syntax.xml import XMLProcessor
from preprocessing.processors.syntax.json import JSONProcessor
from preprocessing.processors.syntax.csv import CSVProcessor
from preprocessing.processors.syntax.markdown import MarkdownProcessor
from preprocessing.processors.semantic.comment import CommentProcessor
from preprocessing.processors.semantic.docstring import DocstringProcessor
from preprocessing.processors.analysis.duplicate import DuplicateProcessor
from preprocessing.processors.analysis.tokenizer import TokenEstimatorProcessor
from preprocessing.processors.metadata.path import PathNormalizer
from preprocessing.processors.metadata.metadata import MetadataProcessor
from preprocessing.domain.file import Language


class PreprocessingManager:
    """
    Thin public facade for the Preprocessing Framework.
    Mirrors the design of the Sources Framework RepositoryManager.
    """

    def __init__(self, cache_db_path: Path | None = None):
        if cache_db_path is None:
            # Default cache path if not provided
            cache_db_path = Path(".aiodoo/preprocessing_cache.sqlite")

        self._cache_store = CacheStore(cache_db_path)
        self._registry = self._build_default_registry()
        self._pipeline = PreprocessingPipeline(self._cache_store, self._registry)

    def _build_default_registry(self) -> ProcessorRegistry:
        registry = ProcessorRegistry()

        # Universal Text
        registry.register_universal(WhitespaceProcessor())
        registry.register_universal(LineEndingProcessor())

        # Syntax Specific
        registry.register_language(Language.PYTHON, PythonProcessor())
        registry.register_language(Language.XML, XMLProcessor())
        registry.register_language(Language.JSON, JSONProcessor())
        registry.register_language(Language.CSV, CSVProcessor())
        registry.register_language(Language.MARKDOWN, MarkdownProcessor())

        # Semantic
        registry.register_language(Language.PYTHON, CommentProcessor())
        registry.register_language(Language.PYTHON, DocstringProcessor())

        # Metadata & Analysis
        registry.register_analysis(PathNormalizer())
        registry.register_analysis(MetadataProcessor())
        registry.register_analysis(DuplicateProcessor())
        registry.register_analysis(TokenEstimatorProcessor())

        registry.freeze()
        return registry

    def normalize(
        self, source_context: RepositoryContext, options: PipelineOptions | None = None
    ) -> PipelineResult:
        """
        Normalize a RepositoryContext, leveraging cache if available.
        """
        options = options or PipelineOptions()
        p_context = PipelineContext(source_context=source_context, options=options)
        return self._pipeline.execute(p_context)

    def validate(self, source_context: RepositoryContext) -> PipelineResult:
        """
        Validate a RepositoryContext against preprocessing rules without mutating or caching.
        """
        options = PipelineOptions(validate_only=True, skip_cache=True)
        p_context = PipelineContext(source_context=source_context, options=options)
        return self._pipeline.execute(p_context)

    def refresh_cache(self, source_context: RepositoryContext) -> PipelineResult:
        """
        Force re-processing and update the cache for the given context.
        """
        options = PipelineOptions(force_reprocess=True)
        p_context = PipelineContext(source_context=source_context, options=options)
        return self._pipeline.execute(p_context)

    def clear_cache(self) -> None:
        """Clear the entire preprocessing cache."""
        self._cache_store.clear()
