import unittest
from aiodoo_datasets.generators.execution.builders.factories.operation_factory import (
    OperationFactory,
)
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class TestOperationFactory(unittest.TestCase):
    def test_validation(self):
        factory = OperationFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)


if __name__ == "__main__":
    unittest.main()
