import unittest
from aiodoo_datasets.generators.execution.protocol import version


class TestProtocolVersion(unittest.TestCase):
    def test_version_constants(self) -> None:
        self.assertIsNotNone(version.protocol_version)
        self.assertIsNotNone(version.schema_version)
        self.assertIsNotNone(version.compatibility_version)

        self.assertIsInstance(version.protocol_version, str)
        self.assertIsInstance(version.schema_version, str)
        self.assertIsInstance(version.compatibility_version, str)


if __name__ == "__main__":
    unittest.main()
