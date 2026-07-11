from aiodoo_datasets.generators.execution.builders.results.dependency_build_result import (
    DependencyBuildResult,
)


class DependencyValidator:
    """Validates ExecutionDependency domain objects."""

    @classmethod
    def validate(cls, result: DependencyBuildResult) -> None:
        pass
