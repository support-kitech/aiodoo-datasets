"""Pipeline Result for Evaluation Generator."""

from dataclasses import dataclass
from typing import Tuple, Any, Optional
from types import MappingProxyType
from aiodoo_datasets.generators.evaluation.protocol.domain.benchmark_protocol import (
    EvaluationProtocol,
)


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """Immutable output container for the evaluation pipeline."""

    dataset: Tuple[EvaluationProtocol, ...]
    statistics: MappingProxyType[str, Any]
    validation_passed: bool
    export_metadata: Optional[MappingProxyType[str, Any]] = None
