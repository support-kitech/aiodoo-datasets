from dataclasses import dataclass
from generators.execution.builders.results.base import BaseBuildResult
from generators.execution.domain.execution_operation import ExecutionOperation


@dataclass(frozen=True, slots=True)
class OperationBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the OperationBuilder."""

    operations: tuple[ExecutionOperation, ...]
