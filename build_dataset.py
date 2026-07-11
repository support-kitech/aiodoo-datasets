#!/usr/bin/env python3
"""AIODOO Datasets v1.0 Final Orchestrator."""

import argparse
import logging
import sys
from pathlib import Path
from types import SimpleNamespace

from generators.planner.pipeline import PlannerPipeline
from generators.coding.pipeline import CodingPipeline
from generators.repair.pipeline import RepairPipeline
from generators.context.pipeline import ContextPipeline

from generators.execution.integration.pipeline import IntegrationPipeline as ExecutionPipeline
from generators.execution.cli.configuration import build_pipeline_context as build_execution_context

from generators.approval.pipeline import ApprovalPipeline
from generators.approval.cli.configuration import build_pipeline_context as build_approval_context

from generators.conversation.pipeline import ConversationPipeline
from generators.conversation.cli.configuration import build_pipeline_context as build_conversation_context

from generators.evaluation.cli.configuration import Configuration as EvalConfig
from generators.evaluation.cli.commands import Commands as EvalCommands

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("build_dataset")


def run_generator(name: str, func, *args, **kwargs) -> None:
    """Run a generator pipeline with error handling."""
    logger.info("=" * 60)
    logger.info(f"Starting {name} Generator...")
    logger.info("=" * 60)
    try:
        # Planner, Coding, Repair return a boolean (True on success)
        # ContextPipeline.run() returns None
        # Execution, Approval, Conversation pipelines return a Result object
        # Evaluation returns None
        result = func(*args, **kwargs)

        # Some pipelines return a boolean success
        if isinstance(result, bool):
            if not result:
                raise RuntimeError(f"{name} pipeline returned False indicating failure.")
                
        if hasattr(result, "status"):
            from generators.common.pipeline.status import PipelineStatus
            if result.status == PipelineStatus.FAILED:
                diagnostics = getattr(result, "diagnostics", [])
                raise RuntimeError(f"{name} pipeline failed. Diagnostics: {diagnostics}")
            elif result.status == PipelineStatus.SKIPPED:
                logger.info(f"{name} Generator skipped execution (expected without full upstream data).")
            else:
                logger.info(f"{name} Generator completed successfully.")
        elif hasattr(result, "success"):
            if not getattr(result, "success"):
                diagnostics = getattr(result, "diagnostics", [])
                error_msg = f"{name} pipeline failed. Diagnostics: {diagnostics}"
                raise RuntimeError(error_msg)
            logger.info(f"{name} Generator completed successfully.")
    except Exception as e:
        logger.error(f"Fatal error in {name} Generator: {e}")
        logger.error("Stopping immediately.")
        sys.exit(1)


def main() -> None:
    """Main orchestration entrypoint."""
    parser = argparse.ArgumentParser(description="AIODOO Datasets v1.0 Orchestrator")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/sources.yaml"),
        help="Path to the primary sources configuration file",
    )
    args = parser.parse_args()

    config_path = args.config
    output_dir = Path("datasets")
    
    # Ensure standard config files are referenced properly based on the base path
    config_dir = config_path.parent
    eval_config_path = config_dir / "generator.yaml"

    if not config_path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)
        
    if not eval_config_path.exists():
        logger.warning(f"Evaluation configuration not found at {eval_config_path}. Evaluation may fail if required.")

    logger.info(f"Initializing AIODOO Dataset build sequence using config: {config_path}")
    logger.info(f"Output directory set to: {output_dir}")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    workers = 4
    resume = False
    reset_checkpoint = True

    # 1. Planner
    run_generator(
        "Planner",
        lambda: PlannerPipeline(
            sources_yaml=config_path,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            reset_checkpoint=reset_checkpoint,
        ).run(),
    )

    # 2. Coding
    run_generator(
        "Coding",
        lambda: CodingPipeline(
            sources_yaml=config_path,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            reset_checkpoint=reset_checkpoint,
        ).run(),
    )

    # 3. Repair
    run_generator(
        "Repair",
        lambda: RepairPipeline(
            sources_yaml=config_path,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            reset_checkpoint=reset_checkpoint,
        ).run(),
    )

    # 4. Context
    run_generator(
        "Context",
        lambda: ContextPipeline(
            config_path=config_path,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            limit=None,
            target_module=None,
        ).run(),
    )

    # Prepare namespace for subsequent generators
    # Execution, Approval, Conversation expect source_dir to point to Odoo source modules
    common_ns = SimpleNamespace(
        source_dir=Path("sources"),
        output_dir=output_dir,
        debug=False,
        fail_fast=True,
    )

    # 5. Execution
    run_generator(
        "Execution",
        lambda: ExecutionPipeline.execute(build_execution_context(common_ns)),
    )

    # 6. Approval
    run_generator(
        "Approval",
        lambda: ApprovalPipeline.generate(build_approval_context(common_ns)),
    )

    # 7. Conversation
    run_generator(
        "Conversation",
        lambda: ConversationPipeline.generate(build_conversation_context(common_ns)),
    )

    # 8. Evaluation
    run_generator(
        "Evaluation",
        lambda: EvalCommands.run_generate(
            EvalConfig.load(str(eval_config_path)), str(output_dir)
        ),
    )

    logger.info("=" * 60)
    logger.info("All pipelines executed successfully.")
    logger.info(f"Final datasets are available in: {output_dir}")
    logger.info("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
