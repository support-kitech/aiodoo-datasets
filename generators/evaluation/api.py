"""Public API for Evaluation Generator."""

import logging
from typing import Dict, Any, Tuple
from types import MappingProxyType

from generators.evaluation.pipeline.pipeline_context import PipelineContext
from generators.evaluation.pipeline.pipeline_result import PipelineResult
from generators.evaluation.pipeline.pipeline import EvaluationPipeline
from generators.evaluation.domain.evaluation import Evaluation
from generators.evaluation.exceptions import EvaluationGeneratorError
from generators.evaluation.validation.dataset_validator import DatasetValidator
from generators.evaluation.validation.evaluation_validator import EvaluationValidator
# Protocol imports removed

logger = logging.getLogger(__name__)


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

    ACT-103: this previously always returned ``True`` (a no-op stub — see
    ecosystem-v2-certification/MASTER_ACTION_LIST.md). It now runs the real,
    fail-fast domain validators (:class:`EvaluationValidator`,
    :class:`DatasetValidator`) against every :class:`Evaluation` aggregate in
    ``dataset`` and returns ``False`` (fail closed) on any violation,
    unexpected element type, or unexpected exception, instead of silently
    reporting success.
    """
    if not dataset:
        logger.error("Evaluation dataset validation rejected an empty dataset.")
        return False

    for item in dataset:
        if not isinstance(item, Evaluation):
            logger.error(
                "Evaluation dataset validation rejected a non-Evaluation element: %r",
                type(item),
            )
            return False

    try:
        for evaluation in dataset:
            EvaluationValidator.validate(evaluation)
        DatasetValidator.validate(tuple(dataset))
    except EvaluationGeneratorError as exc:
        logger.error("Evaluation dataset validation failed: %s", exc)
        return False
    except Exception:
        logger.exception("Evaluation dataset validation raised an unexpected exception.")
        return False

    return True


def export(result: PipelineResult, output_dir: str) -> PipelineResult:
    """
    Export a generated pipeline result to the file system using the shared DatasetWriter.
    """
    return EvaluationPipeline.export(result, output_dir)
