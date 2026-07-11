import unittest

from aiodoo_datasets.generators.context.analysis.graph import (
    ContextNode,
    ContextEdge,
    ContextGraph,
    NodeType,
    LanguageType,
    RelationshipType,
)
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.generation.enums import QueryType, QueryIntent
from aiodoo_datasets.generators.context.ranking.enums import RankingRuleType, RankingScore
from aiodoo_datasets.generators.context.ranking.rules import (
    DefinitionRule,
    InheritanceRule,
    DependencyRule,
    ViewRule,
    SecurityRule,
    ActionRule,
)


class TestRankingRules(unittest.TestCase):
    def setUp(self):
        self.graph = ContextGraph()

        self.n_model = ContextNode(
            "sale.order", "sale", "models/sale_order.py", NodeType.MODEL, LanguageType.PYTHON
        )
        self.n_custom_model = ContextNode(
            "sale.order", "custom_sale", "models/sale_order.py", NodeType.MODEL, LanguageType.PYTHON
        )

        self.n_manifest_sale = ContextNode(
            "sale", "sale", "__manifest__.py", NodeType.MANIFEST, LanguageType.PYTHON
        )
        self.n_manifest_stock = ContextNode(
            "stock", "stock", "__manifest__.py", NodeType.MANIFEST, LanguageType.PYTHON
        )

        self.n_view = ContextNode(
            "view_sale_order_form", "sale", "views/sale_views.xml", NodeType.VIEW, LanguageType.XML
        )
        self.n_field = ContextNode(
            "amount_total", "sale", "models/sale_order.py", NodeType.FIELD, LanguageType.PYTHON
        )

        self.n_acl = ContextNode(
            "access_sale_order",
            "sale",
            "security/ir.model.access.csv",
            NodeType.ACL,
            LanguageType.CSV,
        )
        self.n_action = ContextNode(
            "action_orders", "sale", "views/sale_views.xml", NodeType.ACTION, LanguageType.XML
        )

        for n in [
            self.n_model,
            self.n_custom_model,
            self.n_manifest_sale,
            self.n_manifest_stock,
            self.n_view,
            self.n_field,
            self.n_acl,
            self.n_action,
        ]:
            self.graph.add_node(n)

        self.graph.add_edge(
            ContextEdge(
                self.n_custom_model.node_id, self.n_model.node_id, RelationshipType.INHERITS
            )
        )
        self.graph.add_edge(
            ContextEdge(
                self.n_manifest_stock.node_id,
                self.n_manifest_sale.node_id,
                RelationshipType.DEPENDS,
            )
        )
        self.graph.add_edge(
            ContextEdge(self.n_view.node_id, self.n_field.node_id, RelationshipType.DISPLAYS)
        )
        self.graph.add_edge(
            ContextEdge(self.n_acl.node_id, self.n_model.node_id, RelationshipType.SECURES)
        )
        self.graph.add_edge(
            ContextEdge(self.n_action.node_id, self.n_view.node_id, RelationshipType.TRIGGERS)
        )

    def test_definition_rule(self):
        rule = DefinitionRule()
        query = Query(
            QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, self.n_model.node_id, "sale.order", "NL"
        )
        results = rule.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, self.n_model.node_id)
        self.assertEqual(results[0].score, RankingScore.DEFINITION)
        self.assertEqual(results[0].matched_rule, RankingRuleType.DEFINITION)

    def test_inheritance_rule(self):
        rule = InheritanceRule()
        query = Query(
            QueryType.FIND_MODEL, QueryIntent.FIND_MODEL, self.n_model.node_id, "sale.order", "NL"
        )
        results = rule.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, self.n_custom_model.node_id)
        self.assertEqual(results[0].score, RankingScore.INHERITANCE)

    def test_dependency_rule(self):
        rule = DependencyRule()
        query = Query(
            QueryType.FIND_DEPENDENCY,
            QueryIntent.FIND_DEPENDENCY,
            self.n_manifest_sale.node_id,
            "sale",
            "NL",
        )
        results = rule.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, self.n_manifest_stock.node_id)
        self.assertEqual(results[0].score, RankingScore.DEPENDENCY)

    def test_view_rule(self):
        rule = ViewRule()
        query = Query(
            QueryType.FIND_VIEW, QueryIntent.FIND_VIEW, self.n_field.node_id, "amount_total", "NL"
        )
        results = rule.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, self.n_view.node_id)
        self.assertEqual(results[0].score, RankingScore.VIEW)

    def test_security_rule(self):
        rule = SecurityRule()
        query = Query(
            QueryType.FIND_SECURITY,
            QueryIntent.FIND_SECURITY,
            self.n_model.node_id,
            "sale.order",
            "NL",
        )
        results = rule.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, self.n_acl.node_id)
        self.assertEqual(results[0].score, RankingScore.SECURITY)

    def test_action_rule(self):
        rule = ActionRule()
        query = Query(
            QueryType.FIND_ACTION,
            QueryIntent.FIND_ACTION,
            self.n_view.node_id,
            "view_sale_order_form",
            "NL",
        )
        results = rule.rank(query, self.graph)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].node_id, self.n_action.node_id)
        self.assertEqual(results[0].score, RankingScore.ACTION)


if __name__ == "__main__":
    unittest.main()
