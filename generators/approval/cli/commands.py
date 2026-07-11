"""CLI commands."""

from generators.approval.cli.arguments import parse_args
from generators.approval.cli.configuration import build_pipeline_context
from generators.approval.pipeline import ApprovalPipeline


def run_pipeline(args: list[str] | None = None) -> int:
    """Run the main approval generator pipeline."""
    try:
        parsed_args = parse_args(args)
        context = build_pipeline_context(parsed_args)

        result = ApprovalPipeline.generate(context)

        if result.success and result.statistics:
            print("Pipeline execution completed successfully.")
            return 0
        else:
            print("Pipeline execution failed:")
            for diag in result.diagnostics:
                print(f" - {diag}")
            return 1

    except Exception as e:
        print(f"Fatal error during CLI execution: {e}")
        return 1
