"""CLI Entrypoint for the AIODOO Coding Dataset Generator."""

from pathlib import Path
from aiodoo_datasets.generators.coding.pipeline import CodingPipeline
from aiodoo_datasets.generators.common.cli.arguments import build_base_parser, setup_logging


def main() -> None:
    setup_logging()
    parser = build_base_parser("Generate AIODOO Coding Protocol Datasets.")
    args = parser.parse_args()

    pipeline = CodingPipeline(
        sources_yaml=Path(args.sources),
        output_dir=Path(args.output),
        workers=args.workers,
        resume=args.resume,
        reset_checkpoint=args.reset_checkpoint,
    )

    pipeline.run()


if __name__ == "__main__":
    main()
