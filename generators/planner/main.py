"""CLI Entrypoint for the AIODOO Planner Dataset Generator."""

from pathlib import Path
from generators.planner.pipeline import PlannerPipeline
from generators.common.cli.arguments import build_base_parser, setup_logging


def main():  # type: ignore[no-untyped-def]
    setup_logging()
    parser = build_base_parser("AIODOO Planner Dataset Generator")
    args = parser.parse_args()

    pipeline = PlannerPipeline(
        sources_yaml=Path(args.sources),
        output_dir=Path(args.output),
        workers=args.workers,
        resume=args.resume,
        reset_checkpoint=args.reset_checkpoint,
    )

    pipeline.run()


if __name__ == "__main__":
    main()  # type: ignore[no-untyped-call]
