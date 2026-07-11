"""Validator for phase protocol."""

from generators.execution.protocol.domain.phase_protocol import PhaseProtocol
from generators.execution.validation.stage_protocol_validator import (
    StageProtocolValidator,
)


class PhaseProtocolValidator:
    """Validates PhaseProtocol schema compliance."""

    @staticmethod
    def validate(phase: PhaseProtocol) -> tuple[str, ...]:
        violations = []
        if not phase.phase_id:
            violations.append("PhaseProtocol missing phase_id.")
        if not phase.stages:
            violations.append(f"PhaseProtocol {phase.phase_id} has no stages.")

        for stage in phase.stages:
            violations.extend(StageProtocolValidator.validate(stage))

        return tuple(violations)
