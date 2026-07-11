import unittest
from types import MappingProxyType
from generators.execution.builders.factories.metadata_factory import MetadataFactory
from generators.execution.builders.exceptions import FactoryError


class TestMetadataFactory(unittest.TestCase):
    def test_validation(self) -> None:
        factory = MetadataFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)

    def test_creation(self) -> None:
        factory = MetadataFactory()
        result = factory.create({"a": 1})
        self.assertIsInstance(result, MappingProxyType)


if __name__ == "__main__":
    unittest.main()
