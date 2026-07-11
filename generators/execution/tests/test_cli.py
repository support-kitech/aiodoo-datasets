import unittest
from pathlib import Path
from generators.execution.cli.arguments import parse_args
from generators.execution.cli.configuration import build_pipeline_context


class TestCLI(unittest.TestCase):
    def test_parse_args(self) -> None:
        args = parse_args(["--source-dir", "/tmp/src", "--output-dir", "/tmp/out", "--fail-fast"])
        self.assertEqual(args.source_dir, Path("/tmp/src"))
        self.assertEqual(args.output_dir, Path("/tmp/out"))
        self.assertTrue(args.fail_fast)

    def test_build_pipeline_context(self) -> None:
        args = parse_args(["--source-dir", "/tmp/src", "--output-dir", "/tmp/out"])
        ctx = build_pipeline_context(args)

        self.assertEqual(ctx.export_config.output_directory, Path("/tmp/out"))
        self.assertEqual(ctx.runtime_config.fail_fast, False)
        self.assertEqual(ctx.generator_config.custom_settings["source_dir"], Path("/tmp/src"))


if __name__ == "__main__":
    unittest.main()
