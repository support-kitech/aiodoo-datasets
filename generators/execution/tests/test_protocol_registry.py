import unittest
from aiodoo_datasets.generators.execution.registries.protocol_registry import ProtocolRegistry
from aiodoo_datasets.generators.execution.protocol.mappers.stage_mapper import StageMapper

class TestProtocolRegistry(unittest.TestCase):
    def test_registry_validation(self):
        registry = ProtocolRegistry()
        registry.register(StageMapper())
        
        # Validates without error
        registry.validate()
        
        # Duplicate should fail
        registry.register(StageMapper())
        with self.assertRaises(ValueError):
            registry.validate()

if __name__ == '__main__':
    unittest.main()
