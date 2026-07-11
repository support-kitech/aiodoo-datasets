"""Phase build result."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.planning.domain.execution_phase import ExecutionPhase


@dataclass(frozen=True, slots=True)
class PhaseResult:
    """
    Immutable result from PhaseBuilder.

    Attributes:
        success: Whether the phase generation was successful.
        phases: Ordered tuple of generated phases.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    phases: tuple[ExecutionPhase, ...] = field(default_factory=tuple)
    diagnostics: tuple[str, ...] = field(default_factory=tuple)
