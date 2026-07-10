from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.domain.execution_constraint import ExecutionConstraint

@dataclass(frozen=True, slots=True)
class ConstraintBuildResult(BaseBuildResult):
    """Result from the ConstraintBuilder."""
    constraints: tuple[ExecutionConstraint, ...]
