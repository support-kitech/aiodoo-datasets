import unittest

from aiodoo_datasets.generators.context.analysis.graph import (
    ContextGraph, LanguageType, RelationshipType
)
from aiodoo_datasets.generators.context.analysis.relationships import (
    ContainsRelationship, InheritsRelationship, ComputesRelationship,
    DisplaysRelationship, TriggersRelationship
)
from aiodoo_datasets.generators.context.analysis.knowledge import ContextKnowledge

class TestRelationshipExtractors(unittest.TestCase):
    
    def setUp(self):
        self.graph = ContextGraph()
        self.knowledge = ContextKnowledge(module_name="test_module")
        # In a real scenario, extractors would look at 'knowledge'. 
        # Since they are scaffolding right now returning empty lists, we just ensure they execute cleanly.
        
    def test_contains_extractor(self):
        extractor = ContainsRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.CONTAINS)
        self.assertIn(LanguageType.PYTHON, extractor.supported_languages)
        
        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])

    def test_inherits_extractor(self):
        extractor = InheritsRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.INHERITS)
        
        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])
        
    def test_computes_extractor(self):
        extractor = ComputesRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.COMPUTES)
        
        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])
        
    def test_displays_extractor(self):
        extractor = DisplaysRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.DISPLAYS)
        self.assertIn(LanguageType.XML, extractor.supported_languages)
        
        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])
        
    def test_triggers_extractor(self):
        extractor = TriggersRelationship()
        self.assertEqual(extractor.relation_type, RelationshipType.TRIGGERS)
        
        edges = extractor.extract(self.graph, self.knowledge)
        self.assertEqual(edges, [])

if __name__ == '__main__':
    unittest.main()
