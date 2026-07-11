import unittest

from generators.context.analysis.graph import (
    ContextGraph,
    LanguageType,
    RelationshipType,
)
from generators.context.analysis.relationships import (
    ContainsRelationship,
    InheritsRelationship,
    ComputesRelationship,
    DisplaysRelationship,
    TriggersRelationship,
)
from generators.context.analysis.knowledge import ContextKnowledge


class TestRelationshipExtractors(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = ContextGraph()
        self.knowledge = ContextKnowledge(module_name="test_module")
        # In a real scenario, extractors would look at 'knowledge'.
        # Since they are scaffolding right now returning empty lists, we just ensure they execute cleanly.

    def test_contains_extractor(self) -> None:
        extractor = ContainsRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.CONTAINS)
        self.assertIn(LanguageType.PYTHON, extractor.supported_languages)

        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])

    def test_inherits_extractor(self) -> None:
        extractor = InheritsRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.INHERITS)

        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])

    def test_computes_extractor(self) -> None:
        extractor = ComputesRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.COMPUTES)

        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])

    def test_displays_extractor(self) -> None:
        extractor = DisplaysRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.DISPLAYS)
        self.assertIn(LanguageType.XML, extractor.supported_languages)

        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])

    def test_triggers_extractor(self) -> None:
        extractor = TriggersRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.TRIGGERS)

        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])


if __name__ == "__main__":
    unittest.main()
