from dataclasses import dataclass
from generators.execution.builders.results.base import BaseBuildResult
from generators.execution.domain.execution_dependency import ExecutionDependency


@dataclass(frozen=True, slots=True)
class DependencyBuildResult(BaseBuildResult):  # type: ignore[misc]
    """Result from the DependencyBuilder."""

    dependencies: tuple[ExecutionDependency, ...]
