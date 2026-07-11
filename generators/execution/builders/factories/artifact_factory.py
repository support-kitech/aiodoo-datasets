from aiodoo_datasets.generators.execution.builders.factories.base import BaseFactory
from aiodoo_datasets.generators.execution.analysis.knowledge.artifact_knowledge import (
    ArtifactKnowledge,
)
from aiodoo_datasets.generators.execution.artifacts.artifact import Artifact
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class ArtifactFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = ArtifactKnowledge
    TARGET = Artifact

    def validate(self, knowledge: ArtifactKnowledge) -> None:
        if not knowledge:
            raise FactoryError("Cannot create Artifact from empty knowledge.")

    def create(self, knowledge: ArtifactKnowledge) -> Artifact:
        self.validate(knowledge)
        # Concrete implementation deferred
        raise NotImplementedError()
