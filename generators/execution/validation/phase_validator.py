"""Phase validator."""

from aiodoo_datasets.generators.execution.planning.domain.execution_phase import ExecutionPhase
from aiodoo_datasets.generators.execution.validation.stage_validator import StageValidator

class PhaseValidator:
    """Validator for execution phases."""
    
    @staticmethod
    def validate(phase: ExecutionPhase) -> tuple[str, ...]:
        """Validate a phase and its stages."""
        violations = []
        if not phase.phase_id:
            violations.append("Phase has no phase_id.")
        if not phase.stages:
            violations.append(f"Phase {phase.phase_id} has no stages.")
            
        for stage in phase.stages:
            violations.extend(StageValidator.validate(stage))
            
        return tuple(violations)
