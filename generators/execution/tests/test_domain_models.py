import unittest
from dataclasses import FrozenInstanceError

from aiodoo_datasets.generators.execution.artifacts.python_artifact import (
    PythonArtifact,
    PythonArtifactType,
)
from aiodoo_datasets.generators.execution.environment.environment import ExecutionEnvironment
from aiodoo_datasets.generators.execution.environment.edition import OdooEdition
from aiodoo_datasets.generators.execution.environment.version import OdooVersion

from aiodoo_datasets.generators.execution.domain.execution_operation import (
    ExecutionOperation,
    OperationAction,
)
from aiodoo_datasets.generators.execution.domain.execution_step import ExecutionStep
from aiodoo_datasets.generators.execution.domain.execution_plan import ExecutionPlan


class TestDomainModels(unittest.TestCase):
    def test_artifact_immutability(self) -> None:
        artifact = PythonArtifact(
            module="sale",
            relative_path="models/sale_order.py",
            name="sale.order",
            artifact_type=PythonArtifactType.MODEL,
        )

        with self.assertRaises(FrozenInstanceError):
            artifact.module = "stock"

    def test_environment_immutability(self) -> None:
        env = ExecutionEnvironment(
            version=OdooVersion.V17,
            edition=OdooEdition.COMMUNITY,
            python_dependencies=("requests",),
        )

        with self.assertRaises(FrozenInstanceError):
            env.version = OdooVersion.V18

    def test_domain_model_aggregation(self) -> None:
        artifact = PythonArtifact(
            module="sale",
            relative_path="models/sale_order.py",
            name="sale.order",
            artifact_type=PythonArtifactType.MODEL,
        )

        operation = ExecutionOperation(
            operation_id="op_001",
            action=OperationAction.CREATE,
            target=artifact,
            payload="class SaleOrder(models.Model):",
        )

        step = ExecutionStep(
            step_id="step_123", description="Create sale.order model", operation=operation
        )

        env = ExecutionEnvironment(version=OdooVersion.V17, edition=OdooEdition.ENTERPRISE)

        plan = ExecutionPlan(plan_id="plan_456", environment=env, steps=(step,))

        # Test full immutability tree
        with self.assertRaises(FrozenInstanceError):
            plan.plan_id = "plan_789"

        with self.assertRaises(FrozenInstanceError):
            plan.steps[0].description = "Hacked description"


if __name__ == "__main__":
    unittest.main()
