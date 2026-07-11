"""CLI entry point for Protocol Framework."""

import sys
from typing import Sequence

from protocol.cli.arguments import build_parser
from protocol.cli.commands import (
    run_build,
    run_export,
    run_summary,
    run_validate_schema,
)
from protocol.core.manager import ProtocolManager


def main(argv: Sequence[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    manager = ProtocolManager()

    if args.command == "build":
        return run_build(args, manager)
    elif args.command == "summary":
        return run_summary(args, manager)
    elif args.command == "export":
        return run_export(args, manager)
    elif args.command == "validate-schema":
        return run_validate_schema(args, manager)

    return 1


if __name__ == "__main__":
    sys.exit(main())
