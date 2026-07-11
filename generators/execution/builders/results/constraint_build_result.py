from dataclasses import dataclass
from generators.execution.builders.results.base import BaseBuildResult
from generators.execution.domain.execution_constraint import ExecutionConstraint


@dataclass(frozen=True, slots=True)
class ConstraintBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the ConstraintBuilder."""

    constraints: tuple[ExecutionConstraint, ...]
