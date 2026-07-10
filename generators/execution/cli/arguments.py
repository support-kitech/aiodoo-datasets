"""CLI arguments parsing."""

import argparse
from pathlib import Path

def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="AIODOO Execution Generator")
    
    parser.add_argument(
        "--source-dir",
        type=Path,
        required=True,
        help="Source directory containing Odoo modules"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory for generated datasets"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Fail fast on errors"
    )
    
    return parser.parse_args(args)
