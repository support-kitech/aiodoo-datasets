from generators.execution.builders.factories.base import BaseFactory
from generators.execution.analysis.knowledge.dependency_knowledge import (
    DependencyKnowledge,
)
from generators.execution.domain.execution_dependency import ExecutionDependency
from generators.execution.builders.exceptions import FactoryError


class DependencyFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = DependencyKnowledge
    TARGET = ExecutionDependency

    def validate(self, knowledge: DependencyKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionDependency from empty knowledge.")

    def create(self, knowledge: DependencyKnowledge) -> ExecutionDependency:
        self.validate(knowledge)
        raise NotImplementedError()
