"""Arguments parser for Protocol Framework CLI."""

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="AIODOO Protocol Framework CLI",
        prog="protocol",
    )
    
    # Global options
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--quiet", action="store_true", help="Enable quiet mode")
    
    subparsers = parser.add_subparsers(dest="command", required=True, title="Commands")
    
    # Build command
    build_cmd = subparsers.add_parser("build", help="Build a protocol context")
    build_cmd.add_argument("path", help="Path to input context")
    
    # Summary command
    summary_cmd = subparsers.add_parser("summary", help="Show summary of protocol context")
    summary_cmd.add_argument("path", help="Path to input context")
    
    # Export command
    export_cmd = subparsers.add_parser("export", help="Export protocol context")
    export_cmd.add_argument("path", help="Path to input context")
    export_cmd.add_argument("--format", choices=["json", "jsonl", "dict"], default="json", help="Export format")
    
    # Validate command
    validate_cmd = subparsers.add_parser("validate-schema", help="Validate schema")
    validate_cmd.add_argument("path", help="Path to input context")

    return parser
