"""CLI commands."""

from aiodoo_datasets.generators.execution.cli.arguments import parse_args
from aiodoo_datasets.generators.execution.cli.configuration import build_pipeline_context
from aiodoo_datasets.generators.execution.integration.pipeline import IntegrationPipeline

def run_pipeline(args: list[str] | None = None) -> int:
    """Run the main execution generator pipeline."""
    try:
        parsed_args = parse_args(args)
        context = build_pipeline_context(parsed_args)
        
        result = IntegrationPipeline.execute(context)
        
        if result.success and result.statistics:
            print(f"Pipeline execution completed successfully in {result.statistics.total_execution_time:.2f}s")
            return 0
        else:
            print("Pipeline execution failed:")
            for diag in result.diagnostics:
                print(f" - {diag}")
            return 1
            
    except Exception as e:
        print(f"Fatal error during CLI execution: {e}")
        return 1
