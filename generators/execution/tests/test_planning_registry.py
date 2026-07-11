import unittest
from generators.execution.registries.planning_registry import PlanningRegistry
from generators.execution.planning.builders.stage_builder import StageBuilder


class TestPlanningRegistry(unittest.TestCase):
    def test_registry_validation(self) -> None:
        registry = PlanningRegistry()
        registry.register(StageBuilder())

        # Validates without error
        registry.validate()

        # Duplicate should fail
        registry.register(StageBuilder())
        with self.assertRaises(ValueError):
            registry.validate()


if __name__ == "__main__":
    unittest.main()
