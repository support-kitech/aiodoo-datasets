"""CLI Entrypoint for the Repair Generator."""

import sys
from generators.common.cli.arguments import build_parser
from generators.repair.pipeline import RepairPipeline


def main():  # type: ignore[no-untyped-def]
    parser = build_parser(description="AIODOO Repair Dataset Generator")
    args = parser.parse_args()

    pipeline = RepairPipeline(
        sources_yaml=args.sources,
        output_dir=args.output,
        workers=args.workers,
        resume=args.resume,
        reset_checkpoint=args.reset_checkpoint,
    )

    success = pipeline.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()  # type: ignore[no-untyped-call]
