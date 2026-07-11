from aiodoo_datasets.generators.execution.builders.factories.base import BaseFactory
from aiodoo_datasets.generators.execution.analysis.knowledge.dependency_knowledge import (
    DependencyKnowledge,
)
from aiodoo_datasets.generators.execution.domain.execution_dependency import ExecutionDependency
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class DependencyFactory(BaseFactory):
    SOURCE = DependencyKnowledge
    TARGET = ExecutionDependency

    def validate(self, knowledge: DependencyKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionDependency from empty knowledge.")

    def create(self, knowledge: DependencyKnowledge) -> ExecutionDependency:
        self.validate(knowledge)
        raise NotImplementedError()
