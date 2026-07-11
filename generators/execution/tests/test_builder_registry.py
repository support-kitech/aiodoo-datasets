import unittest
from aiodoo_datasets.generators.execution.registries.builder_registry import BuilderRegistry
from aiodoo_datasets.generators.execution.builders.base import BaseBuilder


class DummyBuilderA(BaseBuilder):
    PRIORITY = 10
    REQUIRES = ()
    INPUT = str
    OUTPUT = int

    def build(self, ctx):
        pass


class DummyBuilderB(BaseBuilder):
    PRIORITY = 20
    REQUIRES = (DummyBuilderA,)
    INPUT = int
    OUTPUT = float

    def build(self, ctx):
        pass


class TestBuilderRegistry(unittest.TestCase):
    def test_valid_registration(self):
        reg = BuilderRegistry()
        reg.register(DummyBuilderB())
        reg.register(DummyBuilderA())
        reg.validate()

        # Priority sort check
        items = reg.items()
        self.assertEqual(items[0].__class__, DummyBuilderA)
        self.assertEqual(items[1].__class__, DummyBuilderB)


if __name__ == "__main__":
    unittest.main()
