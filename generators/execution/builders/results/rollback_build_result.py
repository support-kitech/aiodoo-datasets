from dataclasses import dataclass
from generators.execution.builders.results.base import BaseBuildResult
from generators.execution.domain.execution_rollback import ExecutionRollback


@dataclass(frozen=True, slots=True)
class RollbackBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the RollbackBuilder."""

    rollbacks: tuple[ExecutionRollback, ...]
