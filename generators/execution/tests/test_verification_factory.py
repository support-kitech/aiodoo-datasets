import unittest
from aiodoo_datasets.generators.execution.builders.factories.verification_factory import (
    VerificationFactory,
)
from aiodoo_datasets.generators.execution.builders.exceptions import FactoryError


class TestVerificationFactory(unittest.TestCase):
    def test_validation(self):
        factory = VerificationFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)


if __name__ == "__main__":
    unittest.main()
