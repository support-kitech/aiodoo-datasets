"""CLI Main Entrypoint."""

import sys

from preprocessing.cli.arguments import parse_arguments
from preprocessing.cli.commands import CommandHandler
from preprocessing.core.manager import PreprocessingManager


def main() -> int:
    """Main CLI entry point."""
    args = parse_arguments()
    manager = PreprocessingManager()

    handler = CommandHandler(manager, args)

    try:
        return handler.execute()
    except Exception as e:
        if args.verbose:
            import traceback

            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 4


if __name__ == "__main__":
    sys.exit(main())
