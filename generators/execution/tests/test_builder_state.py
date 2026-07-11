import unittest
from generators.execution.builders.builder_state import BuilderState


class TestBuilderState(unittest.TestCase):
    def test_state_enum(self) -> None:
        self.assertEqual(BuilderState.PENDING.name, "PENDING")
        self.assertEqual(BuilderState.RUNNING.name, "RUNNING")
        self.assertEqual(BuilderState.COMPLETED.name, "COMPLETED")
        self.assertEqual(BuilderState.FAILED.name, "FAILED")
        self.assertEqual(BuilderState.SKIPPED.name, "SKIPPED")


if __name__ == "__main__":
    unittest.main()
