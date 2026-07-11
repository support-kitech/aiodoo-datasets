import unittest
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.artifact_analyzer import ArtifactAnalyzer
from aiodoo_datasets.generators.execution.analysis.operation_analyzer import OperationAnalyzer
from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from aiodoo_datasets.generators.common.discovery.ast_parser import PythonKnowledge
from aiodoo_datasets.generators.common.discovery.xml_parser import XMLKnowledge


class TestAnalyzers(unittest.TestCase):
    def setUp(self):
        self.context = AnalysisContext(
            module=OdooModule(
                name="test", path="", version="17.0", edition="community", manifest={}
            ),
            python_knowledge=PythonKnowledge(),
            xml_knowledge=XMLKnowledge(),
        )

    def test_artifact_analyzer(self):
        analyzer = ArtifactAnalyzer()
        result = analyzer.analyze(self.context)
        self.assertTrue(result.is_successful)

    def test_operation_analyzer(self):
        analyzer = OperationAnalyzer()
        result = analyzer.analyze(self.context)
        self.assertTrue(result.is_successful)


if __name__ == "__main__":
    unittest.main()
