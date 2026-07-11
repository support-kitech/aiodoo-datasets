"""Main CLI entrypoint for Conversation Generator."""

import sys
from aiodoo_datasets.generators.conversation.cli.commands import run_pipeline


def main() -> int:
    """Entry point for the executable."""
    return run_pipeline()


if __name__ == "__main__":
    sys.exit(main())
