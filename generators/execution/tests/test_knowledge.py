import unittest
from dataclasses import FrozenInstanceError
from generators.execution.analysis.knowledge.execution_knowledge import (
    ExecutionKnowledge,
)
from generators.execution.analysis.knowledge.operation_knowledge import (
    OperationKnowledge,
)


class TestKnowledge(unittest.TestCase):
    def test_knowledge_immutability(self) -> None:
        op = OperationKnowledge(artifact_ref_id="art_1", action_type="create")

        ek = ExecutionKnowledge(operations=(op,))

        # Verify knowledge models cannot be modified
        with self.assertRaises(FrozenInstanceError):
            ek.operations = ()


if __name__ == "__main__":
    unittest.main()
