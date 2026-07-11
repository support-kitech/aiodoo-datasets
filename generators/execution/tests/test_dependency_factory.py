import unittest
from aiodoo_datasets.generators.execution.builders.factories.dependency_factory import (
    DependencyFactory,
)
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class TestDependencyFactory(unittest.TestCase):
    def test_validation(self):
        factory = DependencyFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)


if __name__ == "__main__":
    unittest.main()
