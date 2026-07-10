import unittest
from aiodoo_datasets.generators.execution.artifacts.python_artifact import PythonArtifact, PythonArtifactType
from aiodoo_datasets.generators.execution.domain.enums import OperationAction
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation
from aiodoo_datasets.generators.execution.domain.execution_step import ExecutionStep
from aiodoo_datasets.generators.execution.domain.execution_plan import ExecutionPlan
from aiodoo_datasets.generators.execution.domain.execution_metadata import ExecutionMetadata
from aiodoo_datasets.generators.execution.environment.environment import ExecutionEnvironment
from aiodoo_datasets.generators.execution.environment.edition import OdooEdition
from aiodoo_datasets.generators.execution.environment.version import OdooVersion

class TestHashing(unittest.TestCase):
    
    def setUp(self):
        self.artifact = PythonArtifact(
            module="sale",
            relative_path="models/sale.py",
            name="sale.order",
            artifact_type=PythonArtifactType.MODEL
        )
        self.env = ExecutionEnvironment(
            version=OdooVersion.V17,
            edition=OdooEdition.COMMUNITY
        )

    def test_operation_hashing(self):
        op1 = ExecutionOperation(
            operation_id="op_123",
            action=OperationAction.CREATE,
            target=self.artifact
        )
        op2 = ExecutionOperation(
            operation_id="op_123",
            action=OperationAction.UPDATE,
            target=self.artifact
        )
        
        # Only IDs should matter for identity
        self.assertEqual(hash(op1), hash(op2))
        self.assertEqual(op1, op2)
        
    def test_step_hashing(self):
        op = ExecutionOperation(
            operation_id="op_123",
            action=OperationAction.CREATE,
            target=self.artifact
        )
        
        step1 = ExecutionStep(
            step_id="step_abc",
            description="A",
            operation=op,
            metadata=ExecutionMetadata(confidence=1.0)
        )
        
        step2 = ExecutionStep(
            step_id="step_abc",
            description="B",
            operation=op,
            metadata=ExecutionMetadata(confidence=0.5)
        )
        
        self.assertEqual(hash(step1), hash(step2))
        self.assertEqual(step1, step2)

    def test_plan_hashing(self):
        plan1 = ExecutionPlan(
            plan_id="plan_xyz",
            environment=self.env,
            metadata=ExecutionMetadata(generator_version="1.0.0")
        )
        
        plan2 = ExecutionPlan(
            plan_id="plan_xyz",
            environment=self.env,
            metadata=ExecutionMetadata(generator_version="2.0.0")
        )
        
        self.assertEqual(hash(plan1), hash(plan2))
        self.assertEqual(plan1, plan2)

if __name__ == '__main__':
    unittest.main()
