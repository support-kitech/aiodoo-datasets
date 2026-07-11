"""CLI Arguments for Evaluation Generator."""

import argparse


def get_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""
    parser = argparse.ArgumentParser(description="AIODOO Evaluation Dataset Generator")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate an evaluation dataset")
    generate_parser.add_argument(
        "--config", type=str, required=True, help="Path to JSON configuration file"
    )
    generate_parser.add_argument(
        "--output-dir", type=str, required=True, help="Output directory for the generated dataset"
    )

    # Validate command
    validate_parser = subparsers.add_parser(
        "validate", help="Validate an existing evaluation dataset"
    )
    validate_parser.add_argument(
        "--input-dir", type=str, required=True, help="Path to dataset directory"
    )

    return parser
