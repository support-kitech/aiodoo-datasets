"""Registry Freeze Tests for Evaluation Generator."""

import unittest
from aiodoo_datasets.generators.evaluation.registries.factory_registry import FactoryRegistry
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry


class TestRegistryFreeze(unittest.TestCase):
    """Verifies that registries cannot be mutated after freezing."""

    def test_registry_freeze_prevention(self):
        """Ensure modification is blocked after freeze()."""
        # Ensure they are frozen (in a real app, pipeline bootstrap does this)
        FactoryRegistry.freeze()
        ParserRegistry.freeze()

        with self.assertRaises(RuntimeError):
            FactoryRegistry.register("dummy_factory", lambda x: x)

        with self.assertRaises(RuntimeError):
            ParserRegistry.register("dummy_parser", lambda x: x)

        # Verify get_all returns a MappingProxyType (read-only dict)
        factories = FactoryRegistry.get_all()
        with self.assertRaises(TypeError):
            factories["hack"] = "mutated"  # MappingProxyType does not support assignment


if __name__ == "__main__":
    unittest.main()
