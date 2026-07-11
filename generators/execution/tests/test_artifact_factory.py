import unittest
from generators.execution.builders.factories.artifact_factory import ArtifactFactory
from generators.execution.builders.exceptions import FactoryError


class TestArtifactFactory(unittest.TestCase):
    def test_validation(self) -> None:
        factory = ArtifactFactory()
        with self.assertRaises(FactoryError):
            factory.create(None)


if __name__ == "__main__":
    unittest.main()
