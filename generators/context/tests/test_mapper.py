import unittest

from aiodoo_datasets.generators.context.analysis.graph import (
    ContextNode, ContextEdge, ContextGraph, NodeType, LanguageType, RelationshipType
)
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.ranking.enums import RankingRuleType, RankingScore, RankingReason
from aiodoo_datasets.generators.context.ranking.result import RankingResult
from aiodoo_datasets.generators.context.ranking.utils import freeze_metadata
from aiodoo_datasets.generators.context.protocol.mapper import ContextMapper

class TestContextMapper(unittest.TestCase):

    def setUp(self):
        self.graph = ContextGraph()
        self.n_target = ContextNode("sale.order", "sale", "models/sale.py", NodeType.MODEL, LanguageType.PYTHON)
        self.n_artifact = ContextNode("sale.order", "custom_sale", "models/custom.py", NodeType.MODEL, LanguageType.PYTHON)
        self.n_unrelated = ContextNode("stock.picking", "stock", "models/stock.py", NodeType.MODEL, LanguageType.PYTHON)
        
        self.graph.add_node(self.n_target)
        self.graph.add_node(self.n_artifact)
        self.graph.add_node(self.n_unrelated)
        
        self.edge1 = ContextEdge(self.n_artifact.node_id, self.n_target.node_id, RelationshipType.INHERITS)
        self.edge2 = ContextEdge(self.n_unrelated.node_id, self.n_target.node_id, RelationshipType.DEPENDS)
        self.graph.add_edge(self.edge1)
        self.graph.add_edge(self.edge2)
        
        self.query = Query(QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, self.n_target.node_id, "sale.order", "Where?")
        
        self.results = [
            RankingResult(
                query_id=self.query.query_id,
                node_id=self.n_artifact.node_id,
                score=RankingScore.INHERITANCE,
                matched_rule=RankingRuleType.INHERITANCE,
                reason=RankingReason.MODEL_INHERITANCE,
                metadata=freeze_metadata({
                    "start_line": 10,
                    "matched_relationship": RelationshipType.INHERITS.value
                })
            )
        ]
        
        self.mapper = ContextMapper()

    def test_mapper_subgraph_extraction(self):
        task = self.mapper.map(self.query, self.results, self.graph)
        
        # Artifacts
        self.assertEqual(len(task.artifacts), 1)
        self.assertEqual(task.artifacts[0].node_id, self.n_artifact.node_id)
        
        # Minimal subgraph nodes: target + artifact (unrelated is omitted)
        self.assertEqual(len(task.graph.nodes), 2)
        node_ids = {n.node_id for n in task.graph.nodes}
        self.assertIn(self.n_target.node_id, node_ids)
        self.assertIn(self.n_artifact.node_id, node_ids)
        self.assertNotIn(self.n_unrelated.node_id, node_ids)
        
        # Minimal subgraph edges: edge1 only (edge2 omitted because unrelated wasn't ranked)
        self.assertEqual(len(task.graph.edges), 1)
        self.assertEqual(task.graph.edges[0].edge_id, self.edge1.edge_id)
        
        # Metadata
        self.assertEqual(task.metadata.artifact_count, 1)
        self.assertEqual(task.metadata.relationship_count, 1)
        self.assertEqual(task.metadata.module, "sale")

    def test_mapper_read_only(self):
        nodes_before = len(self.graph._nodes)
        edges_before = len(self.graph._edges)
        
        self.mapper.map(self.query, self.results, self.graph)
        
        self.assertEqual(len(self.graph._nodes), nodes_before)
        self.assertEqual(len(self.graph._edges), edges_before)

if __name__ == '__main__':
    unittest.main()
