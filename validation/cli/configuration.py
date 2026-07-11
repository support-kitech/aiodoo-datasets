"""CLI argument parsing for the Validation Framework."""

import argparse
from pathlib import Path

from validation.domain.enums import ReportFormat, ValidationSeverity
from validation.pipeline.pipeline_options import ValidationOptions


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for validation commands."""
    parser = argparse.ArgumentParser(description="AIODOO Dataset Validation CLI")
    subparsers = parser.add_subparsers(dest="command", help="Validation commands")

    # validate-all
    all_parser = subparsers.add_parser("validate-all", help="Validate all datasets")
    _add_common_args(all_parser)

    # validate-dataset
    ds_parser = subparsers.add_parser("validate-dataset", help="Validate a single JSONL file")
    ds_parser.add_argument("file", type=Path, help="Path to JSONL file")
    _add_common_args(ds_parser)

    # validate-record
    rec_parser = subparsers.add_parser("validate-record", help="Validate a single record")
    rec_parser.add_argument("file", type=Path, help="Path to JSONL file")
    rec_parser.add_argument("line", type=int, help="Line number (0-indexed)")

    return parser.parse_args(argv)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to a subparser."""
    parser.add_argument("--dir", type=Path, default=Path("datasets"), help="Dataset directory")
    parser.add_argument(
        "--format",
        type=str,
        choices=["console", "json", "markdown", "ci"],
        default="console",
        help="Report format",
    )
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first FATAL issue")
    parser.add_argument("--workers", type=int, default=4, help="Parallel workers")
    parser.add_argument(
        "--severity",
        type=str,
        choices=["fatal", "error", "warning", "info"],
        default="warning",
        help="Minimum severity to report",
    )


def build_options(args: argparse.Namespace) -> ValidationOptions:
    """Build ValidationOptions from parsed CLI args."""
    return ValidationOptions(
        fail_fast=getattr(args, "fail_fast", False),
        workers=getattr(args, "workers", 4),
        report_format=ReportFormat(getattr(args, "format", "console")),
        severity_threshold=ValidationSeverity(getattr(args, "severity", "warning")),
    )
