from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.domain.execution_rollback import ExecutionRollback

@dataclass(frozen=True, slots=True)
class RollbackBuildResult(BaseBuildResult):
    """Result from the RollbackBuilder."""
    rollbacks: tuple[ExecutionRollback, ...]
