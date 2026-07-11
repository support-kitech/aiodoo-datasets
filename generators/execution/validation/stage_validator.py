"""Stage validator."""

from generators.execution.planning.domain.execution_stage import ExecutionStage


class StageValidator:
    """Validator for execution stages."""

    @staticmethod
    def validate(stage: ExecutionStage) -> tuple[str, ...]:
        """Validate a single stage."""
        violations = []
        if not stage.stage_id:
            violations.append("Stage has no stage_id.")
        if not stage.nodes:
            violations.append(f"Stage {stage.stage_id} has no nodes.")
        return tuple(violations)
