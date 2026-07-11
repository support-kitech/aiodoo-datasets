from generators.execution.builders.results.constraint_build_result import (
    ConstraintBuildResult,
)


class ConstraintValidator:
    """Validates ExecutionConstraint domain objects."""

    @classmethod
    def validate(cls, result: ConstraintBuildResult) -> None:
        pass
