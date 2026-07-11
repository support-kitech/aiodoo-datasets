import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

from aiodoo_datasets.generators.context.pipeline import ContextPipeline, process_module
from aiodoo_datasets.generators.common.discovery.scanner import OdooModule, ManifestInfo


class TestContextPipeline(unittest.TestCase):
    @patch("aiodoo_datasets.generators.context.pipeline.OdooASTParser")
    @patch("aiodoo_datasets.generators.context.pipeline.OdooXMLParser")
    def test_process_module_empty(self, mock_xml, mock_ast):
        # Setup mocks to return empty knowledge
        mock_ast.return_value.parse_module.return_value = MagicMock(files={})
        mock_xml.return_value.parse_module.return_value = MagicMock(files={})

        module = OdooModule(
            name="test_mod",
            path=Path("/fake"),
            version="17.0",
            edition="ce",
            manifest=ManifestInfo(),
        )

        tasks = process_module(module)
        # Empty graph -> 0 queries -> 0 tasks
        self.assertEqual(len(tasks), 0)

    @patch("aiodoo_datasets.generators.context.pipeline.ModuleScanner")
    @patch("aiodoo_datasets.generators.context.pipeline.CheckpointManager")
    def test_pipeline_orchestration(self, mock_chkpt, mock_scanner):
        mock_scanner.return_value.discover_modules.return_value = []

        pipeline = ContextPipeline(config_path="fake.yaml", output_dir="/tmp/out", workers=1)
        pipeline.run()

        # Ensure it attempts discovery
        mock_scanner.return_value.discover_modules.assert_called_once()
        # Should initialize gracefully
        self.assertEqual(pipeline.writer.written_count, 0)


if __name__ == "__main__":
    unittest.main()
