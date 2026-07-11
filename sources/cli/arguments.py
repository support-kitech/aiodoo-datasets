"""CLI Argument definitions."""

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="AIODOO Sources Framework CLI",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    
    parser.add_argument(
        "command",
        choices=["scan", "validate", "summary", "cache-info", "cache-clear", "refresh-cache"],
        help="Command to execute",
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/sources.yaml"),
        help="Path to the primary sources configuration file",
    )
    
    parser.add_argument(
        "--versions",
        type=Path,
        default=Path("config/versions.yaml"),
        help="Path to the framework versions configuration file (if applicable)",
    )

    parser.add_argument(
        "--force-rescan",
        action="store_true",
        help="Force a fresh scan of the repositories, ignoring cache",
    )

    parser.add_argument(
        "--skip-cache",
        action="store_true",
        help="Skip cache interactions entirely (neither read nor write)",
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only run validations without executing full scan/load",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress all non-essential output",
    )

    return parser
