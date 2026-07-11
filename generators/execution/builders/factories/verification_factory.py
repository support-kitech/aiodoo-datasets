from generators.execution.builders.factories.base import BaseFactory
from generators.execution.analysis.knowledge.verification_knowledge import (
    VerificationKnowledge,
)
from generators.execution.domain.execution_verification import ExecutionVerification
from generators.execution.builders.exceptions import FactoryError


class VerificationFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = VerificationKnowledge
    TARGET = ExecutionVerification

    def validate(self, knowledge: VerificationKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create ExecutionVerification from empty knowledge.")

    def create(self, knowledge: VerificationKnowledge) -> ExecutionVerification:
        self.validate(knowledge)
        raise NotImplementedError()
