import unittest
from generators.execution.registries.factory_registry import FactoryRegistry
from generators.execution.builders.factories.base import BaseFactory


class DummyFactoryA(BaseFactory):
    SOURCE = str
    TARGET = int

    def validate(self, knowledge):
        pass

    def create(self, knowledge):
        pass


class DummyFactoryB(BaseFactory):
    SOURCE = str
    TARGET = int

    def validate(self, knowledge):
        pass

    def create(self, knowledge):
        pass


class TestFactoryRegistry(unittest.TestCase):
    def test_duplicate_mapping(self) -> None:
        reg = FactoryRegistry()
        reg.register(DummyFactoryA())
        reg.register(DummyFactoryB())
        with self.assertRaisesRegex(ValueError, "Duplicate factory mapping"):
            reg.validate()


if __name__ == "__main__":
    unittest.main()
