from generators.execution.builders.factories.base import BaseFactory
from generators.execution.analysis.knowledge.constraint_knowledge import (
    ConstraintKnowledge,
)
from generators.execution.domain.execution_constraint import ExecutionConstraint
from generators.execution.builders.exceptions import FactoryError


class ConstraintFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = ConstraintKnowledge
    TARGET = ExecutionConstraint

    def validate(self, knowledge: ConstraintKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionConstraint from empty knowledge.")

    def create(self, knowledge: ConstraintKnowledge) -> ExecutionConstraint:
        self.validate(knowledge)
        raise NotImplementedError()
