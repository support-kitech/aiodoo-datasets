"""CLI entrypoint for Context Generator."""

import sys
import logging
from aiodoo_datasets.generators.common.cli.arguments import build_base_parser, setup_logging
from aiodoo_datasets.generators.context.pipeline import ContextPipeline

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    parser = build_base_parser(description="Generate AIODOO Context Protocol V1 Dataset")
    parser.add_argument("--limit", type=int, help="Maximum number of context records to generate")
    parser.add_argument("--module", type=str, help="Process a single specific module")

    args = parser.parse_args()

    try:
        pipeline = ContextPipeline(
            config_path=args.sources,
            output_dir=args.output,
            workers=args.workers,
            resume=args.resume and not args.reset_checkpoint,
            limit=args.limit,
            target_module=args.module,
        )
        pipeline.run()
    except KeyboardInterrupt:
        logger.info("Generation interrupted by user. State is saved.")
        sys.exit(130)
    except Exception as e:
        logger.exception("Pipeline failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
