"""Integration tests for the complete Approval Pipeline."""

import unittest
from pathlib import Path
import tempfile
from generators.approval.pipeline import ApprovalPipeline
from generators.approval.pipeline_context import PipelineContext
from generators.approval.config.approval_config import ApprovalConfig
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.rules.rule_set import RuleSet
from generators.approval.rules.security_rules import SQLInjectionRule


class TestApprovalPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_path = Path(self.temp_dir.name)

        self.config = ApprovalConfig(
            output_dir=str(self.output_path),
            manifest_path=str(self.output_path / "dataset_manifest.json"),
        )
        self.metadata = ReviewMetadata(
            generator_version="1.0.0",
            protocol_version="1.0",
            schema_version="1.0",
            source_module="account",
            odoo_version="18.0",
            odoo_edition="enterprise",
            complexity_score=10,
        )
        self.rule_set = RuleSet(rules=(SQLInjectionRule(),))

        self.input_protocols = {
            "coding_data": {
                "files": [
                    {
                        "id": "file_1",
                        "path": "test.py",
                        "content": "self.env.cr.execute(f'SELECT * FROM {table}')",
                    }
                ]
            }
        }

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_pipeline_generate(self) -> None:
        context = PipelineContext(
            config=self.config,
            input_protocols=self.input_protocols,
            metadata=self.metadata,
            rule_set=self.rule_set,
        )

        result = ApprovalPipeline.generate(context)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.approval_protocol)
        self.assertEqual(result.statistics["findings_total"], 1)
        self.assertEqual(result.statistics["rejections"], 1)

        # Check deterministic output
        result2 = ApprovalPipeline.generate(context)
        self.assertEqual(result.approval_protocol, result2.approval_protocol)
        self.assertEqual(result.statistics, result2.statistics)
        self.assertEqual(result.approval_protocol.review_id, result2.approval_protocol.review_id)

        # Check export integration
        jsonl_path = self.output_path / "approval_dataset.jsonl"
        self.assertTrue(jsonl_path.exists())

        manifest_path = self.output_path / "dataset_manifest.json"
        self.assertTrue(manifest_path.exists())
