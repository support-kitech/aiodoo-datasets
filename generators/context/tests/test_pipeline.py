import unittest
from unittest.mock import patch, MagicMock

from generators.context.pipeline import ContextPipeline, process_module
from preprocessing.domain.repository import PreprocessedModule


class TestContextPipeline(unittest.TestCase):
    @patch("generators.context.pipeline.OdooASTParser")
    @patch("generators.context.pipeline.OdooXMLParser")
    def test_process_module_empty(self, mock_xml, mock_ast):
        # Setup mocks to return empty knowledge
        mock_ast.return_value.parse_module.return_value = MagicMock(files={})
        mock_xml.return_value.parse_module.return_value = MagicMock(files={})

        module = PreprocessedModule(
            name="test_mod",
            files=[],
            metadata={"path": "/fake"},
        )

        tasks = process_module(module, "test_hash")
        # Empty graph -> 0 queries -> 0 tasks
        self.assertEqual(len(tasks), 0)

    @patch("generators.context.pipeline.CheckpointManager")
    def test_pipeline_orchestration(self, mock_chkpt):

        pipeline = ContextPipeline(
            repository_context=MagicMock(),
            protocol_context=MagicMock(),
            output_dir="/tmp/out",
            workers=1,
        )
        pipeline.run()

        # Should initialize gracefully
        self.assertEqual(pipeline.writer.written_count, 0)


if __name__ == "__main__":
    unittest.main()
