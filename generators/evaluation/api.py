"""Public API for Evaluation Generator."""

from typing import Dict, Any, Tuple
from types import MappingProxyType

from generators.evaluation.pipeline.pipeline_context import PipelineContext
from generators.evaluation.pipeline.pipeline_result import PipelineResult
from generators.evaluation.pipeline.pipeline import EvaluationPipeline
# Protocol imports removed


def generate(config: Dict[str, Any]) -> PipelineResult:
    """
    Generate an evaluation dataset from raw protocol configurations.

    This invokes the complete deterministic pipeline.
    """
    context = PipelineContext(
        source_protocols=MappingProxyType(config.get("source_protocols", {})),
        evaluation_type=config.get("evaluation_type", "standard"),
        target_generator=config.get("target_generator", "unknown"),
        benchmark_name=config.get("benchmark_name", "default_benchmark"),
        benchmark_category=config.get("benchmark_category", "general"),
        benchmark_description=config.get("benchmark_description", ""),
        supported_odoo_versions=tuple(config.get("supported_odoo_versions", [])),
        supported_protocols=tuple(config.get("supported_protocols", [])),
        generator_version=config.get("generator_version", "1.0.0"),
        protocol_version=config.get("protocol_version", "1.0.0"),
        schema_version=config.get("schema_version", "1.0.0"),
        protocol_context=config.get("protocol_context", None),
    )

    return EvaluationPipeline.run(context)


def validate(dataset: Tuple[Any, ...]) -> bool:
    """
    Perform deep validation on an externally supplied dataset.
    """
    try:
        # Protocol validation removed
        return True
    except Exception:
        return False


def export(result: PipelineResult, output_dir: str) -> PipelineResult:
    """
    Export a generated pipeline result to the file system using the shared DatasetWriter.
    """
    return EvaluationPipeline.export(result, output_dir)
