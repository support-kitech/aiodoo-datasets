"""CLI Arguments parsing for the Preprocessing Framework."""

import argparse
from typing import NamedTuple

from preprocessing.pipeline.pipeline_options import PipelineOptions


class CliArgs(NamedTuple):
    """Parsed CLI arguments."""

    command: str
    config: str | None
    force_reprocess: bool
    skip_cache: bool
    validate_only: bool
    verbose: bool
    json_output: bool


def parse_arguments() -> CliArgs:
    """Parse CLI arguments into a structured tuple."""
    parser = argparse.ArgumentParser(
        description="AIODOO Preprocessing Framework CLI.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # normalize command
    norm_parser = subparsers.add_parser("normalize", help="Run full preprocessing normalization")
    norm_parser.add_argument("--config", type=str, help="Path to sources configuration file")

    # validate command
    val_parser = subparsers.add_parser(
        "validate", help="Run Stage 1 & 2 validation without caching"
    )
    val_parser.add_argument("--config", type=str, help="Path to sources configuration file")

    # summary command
    sum_parser = subparsers.add_parser("summary", help="Display preprocessing statistics")
    sum_parser.add_argument("--config", type=str, help="Path to sources configuration file")

    # cache commands
    subparsers.add_parser("cache-info", help="Display cache metadata and statistics")
    subparsers.add_parser("cache-clear", help="Safely delete the preprocessing cache")
    ref_parser = subparsers.add_parser("refresh-cache", help="Force rebuild of the cache")
    ref_parser.add_argument("--config", type=str, help="Path to sources configuration file")

    # benchmark command
    subparsers.add_parser("benchmark", help="Run preprocessing cache benchmark")

    # Global options
    parser.add_argument(
        "--force", action="store_true", help="Force reprocessing even if cache hits"
    )
    parser.add_argument(
        "--skip-cache", action="store_true", help="Completely bypass cache read/writes"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose logging and stack traces"
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress non-error output")
    parser.add_argument(
        "--json", action="store_true", dest="json_output", help="Output purely structured JSON"
    )

    args = parser.parse_args()

    return CliArgs(
        command=args.command,
        config=getattr(args, "config", None),
        force_reprocess=args.force,
        skip_cache=args.skip_cache,
        validate_only=args.command == "validate",
        verbose=args.verbose,
        json_output=args.json_output,
    )


def to_pipeline_options(args: CliArgs) -> PipelineOptions:
    """Convert parsed CLI arguments into PipelineOptions."""
    return PipelineOptions(
        force_reprocess=args.force_reprocess or args.command == "refresh-cache",
        skip_cache=args.skip_cache,
        validate_only=args.validate_only,
    )
