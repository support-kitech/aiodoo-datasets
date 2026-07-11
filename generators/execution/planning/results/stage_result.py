"""Stage build result."""

from dataclasses import dataclass, field
from generators.execution.planning.domain.execution_stage import ExecutionStage


@dataclass(frozen=True, slots=True)
class StageResult:
    """
    Immutable result from StageBuilder.

    Attributes:
        success: Whether the stage generation was successful.
        stages: Ordered tuple of generated stages.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    stages: tuple[ExecutionStage, ...] = field(default_factory=tuple)
    diagnostics: tuple[str, ...] = field(default_factory=tuple)
