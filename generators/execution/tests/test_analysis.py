import unittest
from aiodoo_datasets.generators.execution.analysis.execution_analyzer import ExecutionAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from aiodoo_datasets.generators.common.discovery.ast_parser import PythonKnowledge
from aiodoo_datasets.generators.common.discovery.xml_parser import XMLKnowledge

class TestAnalysisPipeline(unittest.TestCase):
    
    def test_pipeline_execution(self):
        analyzer = ExecutionAnalyzer()
        context = AnalysisContext(
            module=OdooModule(name="test", path="", version="17.0", edition="community", manifest={}),
            python_knowledge=PythonKnowledge(),
            xml_knowledge=XMLKnowledge()
        )
        
        # Run entire pipeline
        knowledge = analyzer.execute(context)
        
        # Verify all tuple containers initialized
        self.assertIsInstance(knowledge.artifacts, tuple)
        self.assertIsInstance(knowledge.operations, tuple)
        self.assertIsInstance(knowledge.dependencies, tuple)
        self.assertIsInstance(knowledge.constraints, tuple)
        self.assertIsInstance(knowledge.verifications, tuple)
        self.assertIsInstance(knowledge.rollbacks, tuple)

if __name__ == '__main__':
    unittest.main()
