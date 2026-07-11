from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation


@dataclass(frozen=True, slots=True)
class OperationBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the OperationBuilder."""

    operations: tuple[ExecutionOperation, ...]
