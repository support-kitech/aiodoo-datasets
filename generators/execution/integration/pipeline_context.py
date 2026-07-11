"""Immutable context for the Integration pipeline."""

from dataclasses import dataclass
from typing import Any
from aiodoo_datasets.generators.execution.config.generator_config import GeneratorConfig
from aiodoo_datasets.generators.execution.config.export_config import ExportConfig
from aiodoo_datasets.generators.execution.config.runtime_config import RuntimeConfig
from aiodoo_datasets.generators.execution.integration.pipeline_statistics import PipelineStatistics


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """
    Context carrying only necessary data for the end-to-end pipeline.

    Attributes:
        generator_config: Immutable generator configuration.
        export_config: Immutable export configuration.
        runtime_config: Immutable runtime configuration.
        discovery_result: The result of the Discovery phase.
        pipeline_statistics: Mutable statistics container for the pipeline.
    """

    generator_config: GeneratorConfig
    export_config: ExportConfig
    runtime_config: RuntimeConfig
    discovery_result: Any
    pipeline_statistics: PipelineStatistics
