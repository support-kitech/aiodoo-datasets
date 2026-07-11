import unittest
from aiodoo_datasets.generators.execution.registries.graph_registry import GraphRegistry


class DummyA:
    pass


class DummyB:
    pass


class TestGraphRegistry(unittest.TestCase):
    def test_valid_registration(self) -> None:
        reg = GraphRegistry()
        reg.register(DummyA())
        reg.register(DummyB())
        reg.validate()  # Should not raise
        self.assertEqual(len(reg.items()), 2)

    def test_duplicate_rejected(self) -> None:
        reg = GraphRegistry()
        reg.register(DummyA())
        reg.register(DummyA())
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            reg.validate()

    def test_snapshot_immutable(self) -> None:
        reg = GraphRegistry()
        reg.register(DummyA())
        snap = reg.snapshot()
        self.assertEqual(len(snap), 1)
        # Snapshot is a tuple — immutable
        self.assertIsInstance(snap, tuple)


if __name__ == "__main__":
    unittest.main()
