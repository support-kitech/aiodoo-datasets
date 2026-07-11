import unittest
import logging

from aiodoo_datasets.generators.context.protocol.schema import (
    ContextTask,
    ProtocolQuery,
    ProtocolArtifact,
    ProtocolNode,
    ProtocolEdge,
    ProtocolGraph,
    ProtocolMetadata,
)
from aiodoo_datasets.generators.context.protocol.enums import (
    ProtocolQueryType,
    ProtocolIntent,
    ProtocolNodeType,
    ProtocolLanguage,
    ProtocolRankingReason,
)
from aiodoo_datasets.generators.context.validation import (
    SchemaValidator,
    ProtocolValidator,
    CoreValidator,
)
from aiodoo_datasets.generators.context.validation.registry import REGISTERED_VALIDATORS
from aiodoo_datasets.generators.context.validation.result import ValidationResult


class TestValidation(unittest.TestCase):
    def setUp(self):
        logging.getLogger(
            "aiodoo_datasets.generators.context.validation.schema_validator"
        ).setLevel(logging.CRITICAL)
        logging.getLogger(
            "aiodoo_datasets.generators.context.validation.protocol_validator"
        ).setLevel(logging.CRITICAL)
        logging.getLogger("aiodoo_datasets.generators.context.validation.core_validator").setLevel(
            logging.CRITICAL
        )

        query = ProtocolQuery(
            query_id="q1",
            query_type=ProtocolQueryType.FIND_MODEL,
            intent=ProtocolIntent.FIND_MODEL,
            natural_language="nl",
            target_node="n1",
            target_symbol="sym",
        )
        artifact = ProtocolArtifact(
            node_id="n2",
            name="sym2",
            type=ProtocolNodeType.MODEL,
            module="m",
            path="p",
            language=ProtocolLanguage.PYTHON,
            start_line=1,
            end_line=2,
            score=100,
            ranking_reason=ProtocolRankingReason.DIRECT_DEFINITION,
        )
        node1 = ProtocolNode(node_id="n1", name="n", type=ProtocolNodeType.MODEL, module="m")
        node2 = ProtocolNode(node_id="n2", name="n", type=ProtocolNodeType.MODEL, module="m")
        edge = ProtocolEdge(edge_id="e1", source_id="n2", target_id="n1", relationship_type="rt")

        self.valid_task = ContextTask(
            id="task1",
            query=query,
            artifacts=[artifact],
            graph=ProtocolGraph(nodes=[node1, node2], edges=[edge]),
            metadata=ProtocolMetadata(
                module="m",
                query_type=ProtocolQueryType.FIND_MODEL,
                artifact_count=1,
                relationship_count=1,
            ),
        )

    def test_validator_registry(self):
        self.assertIn(SchemaValidator, REGISTERED_VALIDATORS)
        self.assertIn(ProtocolValidator, REGISTERED_VALIDATORS)
        self.assertIn(CoreValidator, REGISTERED_VALIDATORS)

    def test_schema_validator(self):
        validator = SchemaValidator()
        result = validator.validate(self.valid_task)
        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result.valid)

    def test_protocol_validator_success(self):
        validator = ProtocolValidator()
        result = validator.validate(self.valid_task)
        self.assertTrue(result.valid)

    def test_protocol_validator_missing_node(self):
        validator = ProtocolValidator()
        task = self.valid_task.model_copy(deep=True)
        # Remove n2 from graph but keep it in artifacts
        task.graph.nodes = [task.graph.nodes[0]]
        result = validator.validate(task)
        self.assertFalse(result.valid)
        self.assertTrue(len(result.errors) > 0)

    def test_protocol_validator_duplicate_artifact(self):
        validator = ProtocolValidator()
        task = self.valid_task.model_copy(deep=True)
        task.artifacts.append(task.artifacts[0])  # Duplicate
        result = validator.validate(task)
        self.assertFalse(result.valid)

    def test_core_validator_success(self):
        validator = CoreValidator()
        result = validator.validate(self.valid_task)
        self.assertTrue(result.valid)

    def test_core_validator_bad_counts(self):
        validator = CoreValidator()
        task = self.valid_task.model_copy(deep=True)
        task.metadata.artifact_count = 99
        result = validator.validate(task)
        self.assertFalse(result.valid)

    def test_core_validator_ordering(self):
        validator = CoreValidator()
        task = self.valid_task.model_copy(deep=True)
        # Add another artifact with higher score, but place it second
        task.artifacts.append(
            ProtocolArtifact(
                node_id="n3",
                name="n",
                type=ProtocolNodeType.MODEL,
                module="m",
                path="p",
                language=ProtocolLanguage.PYTHON,
                start_line=1,
                end_line=2,
                score=110,
                ranking_reason=ProtocolRankingReason.DIRECT_DEFINITION,
            )
        )
        task.graph.nodes.append(
            ProtocolNode(node_id="n3", name="n", type=ProtocolNodeType.MODEL, module="m")
        )
        # 100 then 110 is invalid DESC ordering
        result = validator.validate(task)
        self.assertFalse(result.valid)


if __name__ == "__main__":
    unittest.main()
