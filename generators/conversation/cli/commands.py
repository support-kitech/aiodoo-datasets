"""CLI commands for Conversation Generator."""

from aiodoo_datasets.generators.conversation.cli.arguments import parse_args
from aiodoo_datasets.generators.conversation.cli.configuration import build_pipeline_context
from aiodoo_datasets.generators.conversation.pipeline import ConversationPipeline

def run_pipeline(args: list[str] | None = None) -> int:
    """Run the main conversation generator pipeline."""
    try:
        parsed_args = parse_args(args)
        context = build_pipeline_context(parsed_args)
        
        result = ConversationPipeline.generate(context)
        
        if result.success and result.statistics:
            print("Pipeline execution completed successfully.")
            print(result.statistics.get_summary())
            return 0
        else:
            print("Pipeline execution failed:")
            for diag in result.diagnostics:
                print(f" - {diag}")
            return 1
            
    except Exception as e:
        print(f"Fatal error during CLI execution: {e}")
        return 1
