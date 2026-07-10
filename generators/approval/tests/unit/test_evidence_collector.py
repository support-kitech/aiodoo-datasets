"""Tests for the Evidence Collector."""

import unittest
from aiodoo_datasets.generators.approval.analysis.evidence_collector import EvidenceCollector
from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator

class TestEvidenceCollector(unittest.TestCase):
    def test_collect_evidence(self):
        planner_data = {
            "tasks": [{"id": "t1", "description": "task 1"}]
        }
        coding_data = {
            "files": [{"id": "f1", "path": "models.py", "content": "class Test:"}]
        }
        execution_data = {
            "test_results": [{"id": "tr1", "name": "test_1", "status": "passed"}]
        }
        repair_data = {
            "fixes": [{"id": "fix1", "description": "fixed typo"}]
        }

        evidence_pool = EvidenceCollector.collect({
            "planner_data": planner_data,
            "coding_data": coding_data,
            "execution_data": execution_data,
            "repair_data": repair_data
        })

        self.assertEqual(len(evidence_pool), 4)
        sources = [e.source_generator for e in evidence_pool]
        self.assertIn(SourceGenerator.PLANNER, sources)
        self.assertIn(SourceGenerator.CODING, sources)
        self.assertIn(SourceGenerator.EXECUTION, sources)
        self.assertIn(SourceGenerator.REPAIR, sources)

        # check individual properties
        coding_evidence = next(e for e in evidence_pool if e.source_generator == SourceGenerator.CODING)
        self.assertEqual(coding_evidence.source_reference, "f1")
        self.assertEqual(coding_evidence.file_path, "models.py")

if __name__ == "__main__":
    unittest.main()
