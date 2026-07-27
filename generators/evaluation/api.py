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
    Generate Evaluation capability SFT judgments (+ separate BenchmarkCatalog).

    ``result.dataset`` contains one judgment record per evaluation case.
    ``result.catalog`` is the non-training BenchmarkCatalog artifact.
    """
    from generators.evaluation.version import SCHEMA_VERSION, __version__

    context = PipelineContext(
        source_protocols=MappingProxyType(config.get("source_protocols", {})),
        evaluation_type=config.get("evaluation_type", "standard"),
        target_generator=config.get("target_generator", "unknown"),
        benchmark_name=config.get("benchmark_name", "default_benchmark"),
        benchmark_category=config.get("benchmark_category", "general"),
        benchmark_description=config.get("benchmark_description", ""),
        supported_odoo_versions=tuple(config.get("supported_odoo_versions", [])),
        supported_protocols=tuple(config.get("supported_protocols", [])),
        generator_version=config.get("generator_version", __version__),
        protocol_version=config.get("protocol_version", "1.0.0"),
        schema_version=config.get("schema_version", SCHEMA_VERSION),
        protocol_context=config.get("protocol_context", None),
    )

    return EvaluationPipeline.run(context)


def validate(dataset: Tuple[Any, ...]) -> bool:
    """
    Validate Evaluation pipeline outputs.

    Accepts either:
    - Judgment SFT dict records (v2 grain), or
    - Legacy :class:`Evaluation` aggregates (catalog domain objects).
    """
    if not dataset:
        logger.error("Evaluation dataset validation rejected an empty dataset.")
        return False

    if all(isinstance(item, dict) for item in dataset):
        required = (
            "record_id",
            "candidate_id",
            "evaluation_case_key",
            "candidate",
            "verdict",
            "metadata",
        )
        for item in dataset:
            for field in required:
                if field not in item:
                    logger.error("Evaluation judgment missing required field: %s", field)
                    return False
            if item.get("verdict") not in {"pass", "fail", "inconclusive"}:
                logger.error("Evaluation judgment has invalid verdict: %r", item.get("verdict"))
                return False
        return True

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
