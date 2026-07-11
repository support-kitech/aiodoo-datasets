import unittest
from aiodoo_datasets.generators.execution.builders.factories.constraint_factory import (
    ConstraintFactory,
)
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class TestConstraintFactory(unittest.TestCase):
    def test_validation(self) -> None:
        factory = ConstraintFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)


if __name__ == "__main__":
    unittest.main()
