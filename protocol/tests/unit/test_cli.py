"""Unit tests for CLI commands."""

import unittest
from io import StringIO
import sys

from protocol.cli.arguments import build_parser
from protocol.cli.commands import run_build, run_export, run_summary, run_validate_schema
from protocol.core.manager import ProtocolManager


class TestCLI(unittest.TestCase):

    def setUp(self):
        self.parser = build_parser()
        self.manager = ProtocolManager()
        self.stdout = StringIO()
        self.stderr = StringIO()
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    def tearDown(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def test_run_build(self):
        args = self.parser.parse_args(["build", "test_path"])
        result = run_build(args, self.manager)
        self.assertEqual(result, 0)
        self.assertIn("Protocol Context built successfully", self.stdout.getvalue())

    def test_run_summary(self):
        args = self.parser.parse_args(["summary", "test_path"])
        result = run_summary(args, self.manager)
        self.assertEqual(result, 0)
        self.assertIn("Objects created:", self.stdout.getvalue())

    def test_run_export(self):
        args = self.parser.parse_args(["export", "test_path"])
        result = run_export(args, self.manager)
        self.assertEqual(result, 0)
        self.assertIn("test_path", self.stdout.getvalue())

    def test_run_validate_schema(self):
        args = self.parser.parse_args(["validate-schema", "test_path"])
        result = run_validate_schema(args, self.manager)
        self.assertEqual(result, 0)
        self.assertIn("Schema is valid", self.stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
