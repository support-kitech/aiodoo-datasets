import unittest
from aiodoo_datasets.generators.execution.artifacts.python_artifact import (
    PythonArtifact,
    PythonArtifactType,
)
from aiodoo_datasets.generators.execution.domain.enums import OperationAction
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation
from aiodoo_datasets.generators.execution.domain.execution_step import ExecutionStep


class TestOrdering(unittest.TestCase):
    def setUp(self):
        self.artifact = PythonArtifact(
            module="sale",
            relative_path="models/sale.py",
            name="sale.order",
            artifact_type=PythonArtifactType.MODEL,
        )

    def test_operation_ordering(self):
        op_a = ExecutionOperation(
            operation_id="a_123", action=OperationAction.CREATE, target=self.artifact
        )
        op_b = ExecutionOperation(
            operation_id="b_123", action=OperationAction.CREATE, target=self.artifact
        )

        self.assertLess(op_a, op_b)
        self.assertTrue(op_a < op_b)

        ops = [op_b, op_a]
        self.assertEqual(sorted(ops), [op_a, op_b])

    def test_step_ordering(self):
        op = ExecutionOperation(
            operation_id="op_1", action=OperationAction.CREATE, target=self.artifact
        )

        step_x = ExecutionStep(step_id="step_x", description="desc", operation=op)
        step_y = ExecutionStep(step_id="step_y", description="desc", operation=op)

        self.assertLess(step_x, step_y)
        self.assertTrue(step_x < step_y)

        steps = [step_y, step_x]
        self.assertEqual(sorted(steps), [step_x, step_y])


if __name__ == "__main__":
    unittest.main()
