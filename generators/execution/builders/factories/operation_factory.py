from generators.execution.builders.factories.base import BaseFactory
from generators.execution.analysis.knowledge.operation_knowledge import (
    OperationKnowledge,
)
from generators.execution.domain.execution_operation import ExecutionOperation
from generators.execution.builders.exceptions import FactoryError


class OperationFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = OperationKnowledge
    TARGET = ExecutionOperation

    def validate(self, knowledge: OperationKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionOperation from empty knowledge.")

    def create(self, knowledge: OperationKnowledge) -> ExecutionOperation:
        self.validate(knowledge)
        raise NotImplementedError()
