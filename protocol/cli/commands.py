"""CLI commands for the Protocol Framework."""

import argparse
import sys

from protocol.core.manager import ProtocolManager
from protocol.domain.enums import ExportFormat
from protocol.pipeline.assembly_options import AssemblyOptions


class DummyInputContext:
    """Mock input context for testing."""
    def __init__(self, name: str):
        self.name = name
        self.metadata = {"cli_tool": True}


def run_build(args: argparse.Namespace, manager: ProtocolManager) -> int:
    """Execute the build command."""
    options = AssemblyOptions(
        verbose=args.verbose,
        quiet=args.quiet,
        export_format="json" if args.json else "dict"
    )
    result = manager.assemble(DummyInputContext(args.path), options)
    if result.validation_result.valid:
        if not args.quiet:
            print("Protocol Context built successfully.")
        if args.json and result.export_payload:
            print(result.export_payload)
        return 0
    else:
        print(f"Validation failed: {result.validation_result.errors}", file=sys.stderr)
        return 1


def run_summary(args: argparse.Namespace, manager: ProtocolManager) -> int:
    """Execute the summary command."""
    options = AssemblyOptions(verbose=args.verbose, quiet=args.quiet)
    result = manager.assemble(DummyInputContext(args.path), options)
    stats = result.statistics
    
    if args.json:
        import json
        print(json.dumps({
            "objects_created": stats.objects_created,
            "assembly_duration_ms": stats.assembly_duration_ms,
            "valid": result.validation_result.valid
        }, indent=2))
    else:
        print("=== Protocol Assembly Summary ===")
        print(f"Objects created: {stats.objects_created}")
        print(f"Assembly duration: {stats.assembly_duration_ms:.2f} ms")
        print(f"Valid: {result.validation_result.valid}")
        
    return 0


def run_export(args: argparse.Namespace, manager: ProtocolManager) -> int:
    """Execute the export command."""
    options = AssemblyOptions(verbose=args.verbose, quiet=args.quiet)
    result = manager.assemble(DummyInputContext(args.path), options)
    if not result.protocol_context:
        print("Failed to build context.", file=sys.stderr)
        return 1
        
    fmt = ExportFormat(args.format)
    payload = manager.export(result.protocol_context, fmt)
    print(payload)
    return 0


def run_validate_schema(args: argparse.Namespace, manager: ProtocolManager) -> int:
    """Execute the validate-schema command."""
    options = AssemblyOptions(verbose=args.verbose, quiet=args.quiet)
    result = manager.assemble(DummyInputContext(args.path), options)
    
    if not result.protocol_context:
        print("Build failed.", file=sys.stderr)
        return 1
        
    val_res = manager.validate(result.protocol_context)
    if val_res.valid:
        if not args.quiet:
            print("Schema is valid.")
        return 0
    else:
        print(f"Schema validation failed: {val_res.errors}", file=sys.stderr)
        return 1
