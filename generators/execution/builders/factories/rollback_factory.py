from aiodoo_datasets.generators.execution.builders.factories.base import BaseFactory
from aiodoo_datasets.generators.execution.analysis.knowledge.rollback_knowledge import (
    RollbackKnowledge,
)
from aiodoo_datasets.generators.execution.domain.execution_rollback import ExecutionRollback
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class RollbackFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = RollbackKnowledge
    TARGET = ExecutionRollback

    def validate(self, knowledge: RollbackKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionRollback from empty knowledge.")

    def create(self, knowledge: RollbackKnowledge) -> ExecutionRollback:
        self.validate(knowledge)
        raise NotImplementedError()
