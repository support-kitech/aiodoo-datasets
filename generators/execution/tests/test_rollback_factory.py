import unittest
from aiodoo_datasets.generators.execution.builders.factories.rollback_factory import RollbackFactory
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError

class TestRollbackFactory(unittest.TestCase):
    def test_validation(self):
        factory = RollbackFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)

if __name__ == '__main__':
    unittest.main()
