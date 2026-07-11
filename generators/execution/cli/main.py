"""Main CLI entrypoint."""

import sys
from aiodoo_datasets.generators.execution.cli.commands import run_pipeline


def main() -> int:
    """Entry point for the executable."""
    return run_pipeline()


if __name__ == "__main__":
    sys.exit(main())
