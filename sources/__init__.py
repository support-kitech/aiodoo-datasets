"""
AIODOO Sources Framework

This module acts as the definitive configuration, discovery, and interpretation
layer for all repositories used within the AIODOO dataset generation pipeline.
"""

from sources.core.manager import RepositoryManager
from sources.pipeline.pipeline_options import PipelineOptions
from sources.pipeline.pipeline_result import PipelineResult
from sources.domain.context import RepositoryContext
from sources.domain.repository import Repository
from sources.domain.module import OdooModule
from sources.exceptions import SourcesError
from sources.constants.framework import SOURCES_FRAMEWORK_VERSION

__version__ = SOURCES_FRAMEWORK_VERSION

__all__ = [
    "RepositoryManager",
    "PipelineOptions",
    "PipelineResult",
    "RepositoryContext",
    "Repository",
    "OdooModule",
    "SourcesError",
    "SOURCES_FRAMEWORK_VERSION",
    "__version__",
]
