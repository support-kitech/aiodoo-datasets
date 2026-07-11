from generators.execution.builders.results.rollback_build_result import (
    RollbackBuildResult,
)


class RollbackValidator:
    """Validates ExecutionRollback domain objects."""

    @classmethod
    def validate(cls, result: RollbackBuildResult) -> None:
        pass
