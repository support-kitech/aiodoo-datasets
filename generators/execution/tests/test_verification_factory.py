import unittest
from generators.execution.builders.factories.verification_factory import (
    VerificationFactory,
)
from generators.execution.builders.exceptions import FactoryError


class TestVerificationFactory(unittest.TestCase):
    def test_validation(self) -> None:
        factory = VerificationFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)


if __name__ == "__main__":
    unittest.main()
