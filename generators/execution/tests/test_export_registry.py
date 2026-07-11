import unittest
from generators.execution.registries.export_registry import ExportRegistry
from generators.execution.export.writers.jsonl_writer import JSONLWriter


class TestExportRegistry(unittest.TestCase):
    def test_registry_validation(self) -> None:
        registry = ExportRegistry()
        registry.register(JSONLWriter())

        # Validates without error
        registry.validate()

        # Duplicate should fail
        registry.register(JSONLWriter())
        with self.assertRaises(ValueError):
            registry.validate()


if __name__ == "__main__":
    unittest.main()
