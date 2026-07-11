from generators.execution.builders.factories.base import BaseFactory
from generators.execution.analysis.knowledge.rollback_knowledge import (
    RollbackKnowledge,
)
from generators.execution.domain.execution_rollback import ExecutionRollback
from generators.execution.builders.exceptions import FactoryError


class RollbackFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = RollbackKnowledge
    TARGET = ExecutionRollback

    def validate(self, knowledge: RollbackKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionRollback from empty knowledge.")

    def create(self, knowledge: RollbackKnowledge) -> ExecutionRollback:
        self.validate(knowledge)
        raise NotImplementedError()
