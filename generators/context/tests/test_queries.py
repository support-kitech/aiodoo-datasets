import unittest

from aiodoo_datasets.generators.context.analysis.graph import (
    ContextNode,
    ContextEdge,
    ContextGraph,
    NodeType,
    LanguageType,
    RelationshipType,
)
from aiodoo_datasets.generators.context.generation.enums import QueryType
from aiodoo_datasets.generators.context.generation.queries import (
    FindModelQuery,
    FindFieldQuery,
    FindComputeQuery,
    FindViewQuery,
    FindActionQuery,
    FindMenuQuery,
    FindSecurityQuery,
    FindDependencyQuery,
)


class TestQueries(unittest.TestCase):
    def setUp(self):
        self.graph = ContextGraph()
        # Mock Nodes
        self.n_model = ContextNode(
            "sale.order", "sale", "models/sale_order.py", NodeType.MODEL, LanguageType.PYTHON
        )
        self.n_field = ContextNode(
            "amount_total", "sale", "models/sale_order.py", NodeType.FIELD, LanguageType.PYTHON
        )
        self.n_method = ContextNode(
            "_compute_total", "sale", "models/sale_order.py", NodeType.METHOD, LanguageType.PYTHON
        )
        self.n_view = ContextNode(
            "view_sale_order_form", "sale", "views/sale_views.xml", NodeType.VIEW, LanguageType.XML
        )
        self.n_action = ContextNode(
            "action_orders", "sale", "views/sale_views.xml", NodeType.ACTION, LanguageType.XML
        )
        self.n_menu = ContextNode(
            "menu_sale_orders", "sale", "views/sale_views.xml", NodeType.MENU, LanguageType.XML
        )
        self.n_acl = ContextNode(
            "access_sale_order",
            "sale",
            "security/ir.model.access.csv",
            NodeType.ACL,
            LanguageType.CSV,
        )
        self.n_manifest_sale = ContextNode(
            "sale", "sale", "__manifest__.py", NodeType.MANIFEST, LanguageType.PYTHON
        )
        self.n_manifest_stock = ContextNode(
            "stock", "stock", "__manifest__.py", NodeType.MANIFEST, LanguageType.PYTHON
        )

        # Mock Edges
        self.e_compute = ContextEdge(
            self.n_field.node_id, self.n_method.node_id, RelationshipType.COMPUTES
        )
        self.e_displays = ContextEdge(
            self.n_view.node_id, self.n_field.node_id, RelationshipType.DISPLAYS
        )
        self.e_triggers_action = ContextEdge(
            self.n_action.node_id, self.n_view.node_id, RelationshipType.TRIGGERS
        )
        self.e_triggers_menu = ContextEdge(
            self.n_menu.node_id, self.n_action.node_id, RelationshipType.TRIGGERS
        )
        self.e_secures = ContextEdge(
            self.n_acl.node_id, self.n_model.node_id, RelationshipType.SECURES
        )
        self.e_depends = ContextEdge(
            self.n_manifest_sale.node_id, self.n_manifest_stock.node_id, RelationshipType.DEPENDS
        )

        # Populate graph
        for node in [
            self.n_model,
            self.n_field,
            self.n_method,
            self.n_view,
            self.n_action,
            self.n_menu,
            self.n_acl,
            self.n_manifest_sale,
            self.n_manifest_stock,
        ]:
            self.graph.add_node(node)
        for edge in [
            self.e_compute,
            self.e_displays,
            self.e_triggers_action,
            self.e_triggers_menu,
            self.e_secures,
            self.e_depends,
        ]:
            self.graph.add_edge(edge)

    def test_find_model_query(self):
        plugin = FindModelQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_MODEL)
        self.assertEqual(queries[0].natural_language, "Where is model sale.order defined?")
        self.assertEqual(queries[0].target_node, self.n_model.node_id)

    def test_find_field_query(self):
        plugin = FindFieldQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_FIELD)
        self.assertEqual(queries[0].natural_language, "Where is field amount_total defined?")

    def test_find_compute_query(self):
        plugin = FindComputeQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_COMPUTE)
        self.assertEqual(queries[0].natural_language, "Where is field amount_total computed?")
        self.assertEqual(queries[0].target_node, self.n_field.node_id)

    def test_find_view_query(self):
        plugin = FindViewQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_VIEW)
        self.assertEqual(queries[0].natural_language, "Which view displays amount_total?")
        self.assertEqual(queries[0].target_node, self.n_field.node_id)

    def test_find_action_query(self):
        plugin = FindActionQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_ACTION)
        self.assertEqual(queries[0].natural_language, "Which action opens view_sale_order_form?")
        self.assertEqual(queries[0].target_node, self.n_view.node_id)

    def test_find_menu_query(self):
        plugin = FindMenuQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_MENU)
        self.assertEqual(queries[0].natural_language, "Which menu opens action_orders?")
        self.assertEqual(queries[0].target_node, self.n_action.node_id)

    def test_find_security_query(self):
        plugin = FindSecurityQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_SECURITY)
        self.assertEqual(queries[0].natural_language, "Which ACL protects sale.order?")
        self.assertEqual(queries[0].target_node, self.n_model.node_id)

    def test_find_dependency_query(self):
        plugin = FindDependencyQuery()
        queries = plugin.generate(self.graph)
        self.assertEqual(len(queries), 1)
        self.assertEqual(queries[0].query_type, QueryType.FIND_DEPENDENCY)
        self.assertEqual(queries[0].natural_language, "Which modules depend on stock?")
        self.assertEqual(queries[0].target_node, self.n_manifest_stock.node_id)


if __name__ == "__main__":
    unittest.main()
