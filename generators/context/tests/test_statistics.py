import unittest
import json
from aiodoo_datasets.generators.context.statistics.context_statistics import ContextStatistics
from aiodoo_datasets.generators.context.protocol.schema import (
    ContextTask, ProtocolQuery, ProtocolArtifact, ProtocolNode, ProtocolEdge, ProtocolGraph, ProtocolMetadata
)
from aiodoo_datasets.generators.context.protocol.enums import (
    ProtocolQueryType, ProtocolIntent, ProtocolNodeType, ProtocolLanguage, ProtocolRankingReason
)

class TestContextStatistics(unittest.TestCase):

    def test_statistics_accumulation(self):
        stats = ContextStatistics()
        
        query = ProtocolQuery(query_id="q1", query_type=ProtocolQueryType.FIND_MODEL, intent=ProtocolIntent.FIND_MODEL, natural_language="nl", target_node="n1", target_symbol="sym")
        artifact = ProtocolArtifact(node_id="n2", name="sym2", type=ProtocolNodeType.MODEL, module="m", path="p", language=ProtocolLanguage.PYTHON, start_line=1, end_line=2, score=100, ranking_reason=ProtocolRankingReason.DIRECT_DEFINITION)
        node1 = ProtocolNode(node_id="n1", name="n", type=ProtocolNodeType.MODEL, module="m")
        node2 = ProtocolNode(node_id="n2", name="n", type=ProtocolNodeType.MODEL, module="m")
        edge = ProtocolEdge(edge_id="e1", source_id="n2", target_id="n1", relationship_type="rt")
        
        task = ContextTask(
            id="task1",
            query=query,
            artifacts=[artifact],
            graph=ProtocolGraph(nodes=[node1, node2], edges=[edge]),
            metadata=ProtocolMetadata(module="m", query_type=ProtocolQueryType.FIND_MODEL, artifact_count=1, relationship_count=1)
        )
        
        stats.add_sample(task, '{"dummy": "json"}')
        
        self.assertEqual(stats.queries_generated, 1)
        self.assertEqual(stats.nodes_discovered, 2)
        self.assertEqual(stats.edges_discovered, 1)
        self.assertEqual(stats.ranking_results, 1)
        
        export_data = stats.get_export_stats()
        self.assertEqual(export_data["average_artifacts_per_query"], 1.0)
        self.assertEqual(export_data["average_relationships_per_query"], 1.0)
        self.assertEqual(export_data["query_type_counts"][ProtocolQueryType.FIND_MODEL.value], 1)

if __name__ == '__main__':
    unittest.main()
