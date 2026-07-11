import unittest
from pydantic import ValidationError
from generators.context.protocol.schema import (
    ContextTask,
    ProtocolQuery,
    ProtocolMetadata,
    ProtocolGraph,
    ProtocolArtifact,
    ProtocolNode,
    ProtocolEdge,
)
from generators.context.protocol.constants import CONTEXT_PROTOCOL_V1
from generators.context.protocol.enums import (
    ProtocolQueryType,
    ProtocolIntent,
    ProtocolNodeType,
    ProtocolLanguage,
    ProtocolRankingReason,
)


class TestProtocol(unittest.TestCase):
    def test_schema_instantiation(self) -> None:
        query = ProtocolQuery(
            query_id="q1",
            query_type=ProtocolQueryType.FIND_MODEL,
            intent=ProtocolIntent.FIND_MODEL,
            natural_language="Where is model?",
            target_node="n1",
            target_symbol="model",
        )

        metadata = ProtocolMetadata(
            module="sale",
            query_type=ProtocolQueryType.FIND_MODEL,
            artifact_count=0,
            relationship_count=0,
            protocol_hash="test_hash"
        )

        graph = ProtocolGraph(nodes=[], edges=[])

        task = ContextTask(id="t1", query=query, artifacts=[], graph=graph, metadata=metadata)

        self.assertEqual(task.id, "t1")
        self.assertEqual(task.metadata.protocol_version, CONTEXT_PROTOCOL_V1)

    def test_missing_fields(self) -> None:
        with self.assertRaises(ValidationError):
            ProtocolQuery(
                query_id="q1",
                # missing query_type
                intent=ProtocolIntent.FIND_MODEL,
                natural_language="Where is model?",
                target_node="n1",
                target_symbol="model",
            )

    def test_protocol_equality_and_hashing(self) -> None:
        # Test ProtocolArtifact
        a1 = ProtocolArtifact(
            node_id="n1",
            name="a",
            type=ProtocolNodeType.MODEL,
            module="m",
            path="p",
            language=ProtocolLanguage.PYTHON,
            start_line=1,
            end_line=2,
            score=100,
            ranking_reason=ProtocolRankingReason.DIRECT_DEFINITION,
        )
        a2 = ProtocolArtifact(
            node_id="n1",
            name="b",
            type=ProtocolNodeType.FIELD,
            module="m2",
            path="p2",
            language=ProtocolLanguage.XML,
            start_line=3,
            end_line=4,
            score=90,
            ranking_reason=ProtocolRankingReason.MODEL_INHERITANCE,
        )
        a3 = ProtocolArtifact(
            node_id="n2",
            name="a",
            type=ProtocolNodeType.MODEL,
            module="m",
            path="p",
            language=ProtocolLanguage.PYTHON,
            start_line=1,
            end_line=2,
            score=100,
            ranking_reason=ProtocolRankingReason.DIRECT_DEFINITION,
        )

        self.assertEqual(a1, a2)  # Equality based only on node_id
        self.assertNotEqual(a1, a3)
        self.assertEqual(hash(a1), hash(a2))
        self.assertNotEqual(hash(a1), hash(a3))

        # Test ProtocolNode
        n1 = ProtocolNode(node_id="n1", name="a", type=ProtocolNodeType.MODEL, module="m")
        n2 = ProtocolNode(node_id="n1", name="b", type=ProtocolNodeType.FIELD, module="m2")
        self.assertEqual(n1, n2)
        self.assertEqual(hash(n1), hash(n2))

        # Test ProtocolEdge
        e1 = ProtocolEdge(edge_id="e1", source_id="s", target_id="t", relationship_type="r")
        e2 = ProtocolEdge(edge_id="e1", source_id="x", target_id="y", relationship_type="z")
        self.assertEqual(e1, e2)
        self.assertEqual(hash(e1), hash(e2))


if __name__ == "__main__":
    unittest.main()
