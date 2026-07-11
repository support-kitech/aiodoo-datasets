"""Unit tests for the CLI."""

import unittest
from unittest.mock import patch, MagicMock

from preprocessing.cli.arguments import parse_arguments
from preprocessing.cli.commands import CommandHandler
from preprocessing.core.manager import PreprocessingManager
from preprocessing.pipeline.pipeline_result import PipelineResult
from preprocessing.pipeline.pipeline_statistics import PipelineStatistics


class TestCLI(unittest.TestCase):
    @patch("sys.argv", ["aiodoo-prep", "normalize"])
    def test_arguments_normalize(self):
        args = parse_arguments()
        self.assertEqual(args.command, "normalize")
        self.assertFalse(args.validate_only)
        self.assertFalse(args.force_reprocess)

    @patch("sys.argv", ["aiodoo-prep", "--json", "validate"])
    def test_arguments_validate(self):
        args = parse_arguments()
        self.assertEqual(args.command, "validate")
        self.assertTrue(args.validate_only)
        self.assertTrue(args.json_output)

    def test_command_handler_success(self):
        manager = MagicMock(spec=PreprocessingManager)

        # Mocking normalize response
        stats = PipelineStatistics(repositories_processed=1, files_processed=5, cache_hit=True)
        res = PipelineResult(success=True, context=MagicMock(), statistics=stats)
        manager.normalize.return_value = res

        from preprocessing.cli.arguments import CliArgs

        args = CliArgs(
            command="normalize",
            config=None,
            force_reprocess=False,
            skip_cache=False,
            validate_only=False,
            verbose=False,
            json_output=False,
        )

        handler = CommandHandler(manager, args)
        handler._get_source_context = MagicMock()

        exit_code = handler.execute()
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
