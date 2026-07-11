"""CLI Main Entrypoint for Evaluation Generator."""

import sys
from generators.evaluation.cli.arguments import get_parser
from generators.evaluation.cli.configuration import Configuration
from generators.evaluation.cli.commands import Commands


def main() -> None:
    """Main CLI entrypoint."""
    parser = get_parser()
    args = parser.parse_args()

    if args.command == "generate":
        config = Configuration.load(args.config)
        Commands.run_generate(config, args.output_dir)
    elif args.command == "validate":
        Commands.run_validate(args.input_dir)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
