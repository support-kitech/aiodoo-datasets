from aiodoo_datasets.generators.execution.builders.factories.base import BaseFactory
from aiodoo_datasets.generators.execution.analysis.knowledge.operation_knowledge import (
    OperationKnowledge,
)
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class OperationFactory(BaseFactory):
    SOURCE = OperationKnowledge
    TARGET = ExecutionOperation

    def validate(self, knowledge: OperationKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionOperation from empty knowledge.")

    def create(self, knowledge: OperationKnowledge) -> ExecutionOperation:
        self.validate(knowledge)
        raise NotImplementedError()
