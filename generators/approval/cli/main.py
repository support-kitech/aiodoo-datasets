"""Main CLI entrypoint."""

import sys
from generators.approval.cli.commands import run_pipeline


def main() -> int:
    """Entry point for the executable."""
    return run_pipeline()  # type: ignore[no-any-return]


if __name__ == "__main__":
    sys.exit(main())
