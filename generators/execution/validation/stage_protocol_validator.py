"""Validator for stage protocol."""

from aiodoo_datasets.generators.execution.protocol.domain.stage_protocol import StageProtocol


class StageProtocolValidator:
    """Validates StageProtocol schema compliance."""

    @staticmethod
    def validate(stage: StageProtocol) -> tuple[str, ...]:
        violations = []
        if not stage.stage_id:
            violations.append("StageProtocol missing stage_id.")
        if not stage.stage_type:
            violations.append("StageProtocol missing stage_type.")
        if not stage.nodes:
            violations.append(f"StageProtocol {stage.stage_id} has no nodes.")
        return tuple(violations)
