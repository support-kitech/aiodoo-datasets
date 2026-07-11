import unittest
from aiodoo_datasets.generators.execution.graph.builder import GraphBuilder
from aiodoo_datasets.generators.execution.graph.context import GraphContext
from aiodoo_datasets.generators.execution.graph.enums import EdgeType
from aiodoo_datasets.generators.execution.domain.execution_step import ExecutionStep
from aiodoo_datasets.generators.execution.domain.execution_operation import ExecutionOperation
from aiodoo_datasets.generators.execution.domain.execution_dependency import ExecutionDependency
from aiodoo_datasets.generators.execution.domain.enums import OperationAction
from aiodoo_datasets.generators.execution.artifacts.python_artifact import PythonArtifact
from aiodoo_datasets.generators.execution.artifacts.enums import PythonArtifactType
from unittest.mock import Mock


class TestGraphBuilder(unittest.TestCase):
    def _make_step(self, step_id, deps=()):
        artifact = PythonArtifact(
            module="test", relative_path="m.py", name="m", artifact_type=PythonArtifactType.MODEL
        )
        op = ExecutionOperation(
            operation_id=f"op_{step_id}", action=OperationAction.CREATE, target=artifact
        )
        return ExecutionStep(
            step_id=step_id, description=f"Step {step_id}", operation=op, dependencies=deps
        )

    def test_deterministic_build(self):
        s1 = self._make_step("s1")
        s2 = self._make_step("s2", deps=(ExecutionDependency(depends_on_step_id="s1"),))
        ctx = GraphContext(builder_context=Mock(), domain_steps=(s1, s2))

        builder = GraphBuilder()
        result = builder.build(ctx)

        self.assertTrue(result.success)
        self.assertEqual(result.statistics.node_count, 2)
        self.assertEqual(result.statistics.edge_count, 1)
        self.assertEqual(len(result.graph.nodes), 2)
        self.assertEqual(len(result.graph.edges), 1)
        self.assertEqual(result.graph.edges[0].edge_type, EdgeType.DEPENDENCY)

    def test_empty_graph(self):
        ctx = GraphContext(builder_context=Mock())
        result = GraphBuilder().build(ctx)
        self.assertTrue(result.success)
        self.assertEqual(result.statistics.node_count, 0)

    def test_determinism(self):
        s1 = self._make_step("s1")
        s2 = self._make_step("s2", deps=(ExecutionDependency(depends_on_step_id="s1"),))
        ctx = GraphContext(builder_context=Mock(), domain_steps=(s1, s2))
        r1 = GraphBuilder().build(ctx)
        r2 = GraphBuilder().build(ctx)
        self.assertEqual(
            tuple(n.node_id for n in r1.graph.nodes), tuple(n.node_id for n in r2.graph.nodes)
        )


if __name__ == "__main__":
    unittest.main()
