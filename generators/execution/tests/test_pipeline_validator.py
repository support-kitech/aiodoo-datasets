import unittest
from pathlib import Path
from aiodoo_datasets.generators.execution.validation.pipeline_validator import PipelineValidator
from aiodoo_datasets.generators.execution.integration.pipeline_result import PipelineResult
from aiodoo_datasets.generators.execution.export.export_result import ExportResult


class TestPipelineValidator(unittest.TestCase):
    def test_validation_failure_no_export(self):
        result = PipelineResult(success=True, export_result=None)
        violations = PipelineValidator.validate(result)
        self.assertIn("Validation failed: Export was not successful.", violations)

    def test_validation_success(self):
        export_result = ExportResult(
            success=True, exported_files=(Path("test.jsonl"),), record_count=1
        )
        result = PipelineResult(success=True, export_result=export_result)
        violations = PipelineValidator.validate(result)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    unittest.main()
