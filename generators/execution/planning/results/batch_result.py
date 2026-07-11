"""Batch build result."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.planning.domain.execution_batch import ExecutionBatch


@dataclass(frozen=True, slots=True)
class BatchResult:
    """
    Immutable result from BatchBuilder.

    Attributes:
        success: Whether the batch generation was successful.
        batches: Ordered tuple of generated batches.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    batches: tuple[ExecutionBatch, ...] = field(default_factory=tuple)
    diagnostics: tuple[str, ...] = field(default_factory=tuple)
