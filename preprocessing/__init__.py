"""
AIODOO Preprocessing Framework

This module provides the central public API for the Preprocessing Framework,
which acts as a universal normalization layer mapping raw `RepositoryContext`
graphs to strictly immutable, uniformly formatted `PreprocessedRepositoryContext` graphs.
"""

from preprocessing.constants.framework import PREPROCESSING_FRAMEWORK_VERSION
from preprocessing.exceptions import PreprocessingError
from preprocessing.pipeline.pipeline_options import PipelineOptions
from preprocessing.pipeline.pipeline_result import PipelineResult
from preprocessing.pipeline.pipeline_statistics import PipelineStatistics
from preprocessing.domain.context import PreprocessedRepositoryContext
from preprocessing.domain.repository import PreprocessedRepository, PreprocessedModule
from preprocessing.domain.file import NormalizedFile, DuplicateStatus, Language
from preprocessing.domain.stats import TransformationStatistics
from preprocessing.core.manager import PreprocessingManager

__version__ = PREPROCESSING_FRAMEWORK_VERSION

__all__ = [
    "PREPROCESSING_FRAMEWORK_VERSION",
    "__version__",
    "PreprocessingError",
    "PipelineOptions",
    "PipelineResult",
    "PipelineStatistics",
    "PreprocessedRepositoryContext",
    "PreprocessedRepository",
    "PreprocessedModule",
    "NormalizedFile",
    "DuplicateStatus",
    "Language",
    "TransformationStatistics",
    "PreprocessingManager",
]
