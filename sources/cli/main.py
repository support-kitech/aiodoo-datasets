"""Main entrypoint for the Sources Framework CLI."""

import sys
from pathlib import Path

from sources.cli.arguments import build_parser
from sources.cli.commands import CliCommands
from sources.core.manager import RepositoryManager
from sources.pipeline.pipeline_options import PipelineOptions
from sources.exceptions import SourcesError


def main() -> None:
    """Execute the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    # We define a common cache location for CLI tools
    # When integrated into build_dataset.py, it might use a different one
    # We will use .aiodoo_cache/sources.sqlite in the project root
    cache_db_path = Path(".aiodoo_cache/sources.sqlite")
    cache_db_path.parent.mkdir(parents=True, exist_ok=True)

    manager = RepositoryManager(cache_db_path)
    options = PipelineOptions(
        force_rescan=args.force_rescan,
        skip_cache=args.skip_cache,
        validate_only=args.validate_only,
    )

    cli = CliCommands(manager, args.config, args.json)

    try:
        if args.command == "scan":
            cli.scan(options)
        elif args.command == "validate":
            cli.validate(options)
        elif args.command == "summary":
            cli.summary(options)
        elif args.command == "cache-info":
            cli.cache_info(options)
        elif args.command == "cache-clear":
            cli.cache_clear(options)
        elif args.command == "refresh-cache":
            cli.refresh_cache(options)
    except SourcesError as e:
        if args.json:
            import json

            print(json.dumps({"success": False, "errors": [str(e)]}))
        else:
            print(f"✗ Fatal Sources Framework Error: {e}")
            if args.verbose:
                import traceback

                traceback.print_exc()
        sys.exit(4)
    except Exception as e:
        if args.json:
            import json

            print(json.dumps({"success": False, "errors": [str(e)]}))
        else:
            print(f"✗ Unexpected Fatal Error: {e}")
            if args.verbose:
                import traceback

                traceback.print_exc()
        sys.exit(4)


if __name__ == "__main__":
    main()
