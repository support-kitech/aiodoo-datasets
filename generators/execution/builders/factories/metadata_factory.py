from types import MappingProxyType
from aiodoo_datasets.generators.execution.builders.factories.base import BaseFactory
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class MetadataFactory(BaseFactory):  # type: ignore[misc]
    SOURCE = dict
    TARGET = MappingProxyType

    def validate(self, knowledge: dict) -> None:  # type: ignore[type-arg]
        if not isinstance(knowledge, dict):
            raise FactoryError("Cannot create MappingProxyType from non-dict.")

    def create(self, knowledge: dict) -> MappingProxyType:  # type: ignore[type-arg]
        self.validate(knowledge)
        return MappingProxyType(knowledge)
