import unittest
from aiodoo_datasets.generators.execution.registries.export_registry import ExportRegistry
from aiodoo_datasets.generators.execution.export.writers.jsonl_writer import JSONLWriter

class TestExportRegistry(unittest.TestCase):
    def test_registry_validation(self):
        registry = ExportRegistry()
        registry.register(JSONLWriter())
        
        # Validates without error
        registry.validate()
        
        # Duplicate should fail
        registry.register(JSONLWriter())
        with self.assertRaises(ValueError):
            registry.validate()

if __name__ == '__main__':
    unittest.main()
