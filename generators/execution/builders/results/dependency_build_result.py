from dataclasses import dataclass
from aiodoo_datasets.generators.execution.builders.results.base import BaseBuildResult
from aiodoo_datasets.generators.execution.domain.execution_dependency import ExecutionDependency


@dataclass(frozen=True, slots=True)
class DependencyBuildResult(BaseBuildResult):
    """Result from the DependencyBuilder."""

    dependencies: tuple[ExecutionDependency, ...]
