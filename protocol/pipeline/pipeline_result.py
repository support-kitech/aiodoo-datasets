"""Pipeline result for the Protocol Framework."""

from dataclasses import dataclass
from typing import Any

from protocol.domain.dataset import ProtocolContext
from protocol.pipeline.pipeline_statistics import PipelineStatistics
from protocol.validation.base import ValidationResult


@dataclass(frozen=True, slots=True)
class PipelineResult:
    """
    Immutable result of the protocol assembly pipeline.
    """

    protocol_context: ProtocolContext | None
    validation_result: ValidationResult
    statistics: PipelineStatistics
    export_payload: str | dict[str, Any] | None = None
