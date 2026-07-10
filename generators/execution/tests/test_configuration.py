import unittest
from pathlib import Path
from aiodoo_datasets.generators.execution.config.generator_config import GeneratorConfig
from aiodoo_datasets.generators.execution.config.export_config import ExportConfig
from aiodoo_datasets.generators.execution.config.runtime_config import RuntimeConfig

class TestConfiguration(unittest.TestCase):
    def test_generator_config_immutability(self):
        config = GeneratorConfig(version="1.0.0")
        with self.assertRaises(Exception):
            config.version = "2.0.0"  # Should raise dataclass FrozenInstanceError
            
    def test_export_config_defaults(self):
        config = ExportConfig(output_directory=Path("/tmp"))
        self.assertTrue(config.generate_manifest)
        self.assertTrue(config.generate_metadata)
        
    def test_runtime_config_defaults(self):
        config = RuntimeConfig()
        self.assertFalse(config.debug_mode)
        self.assertTrue(config.fail_fast)

if __name__ == '__main__':
    unittest.main()
