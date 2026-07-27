#!/usr/bin/env python3
"""AIODOO Datasets v1.0 Final Orchestrator."""

import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any

from generators.planner.pipeline import PlannerPipeline
from generators.coding.pipeline import CodingPipeline
from generators.repair.pipeline import RepairPipeline
from generators.context.pipeline import ContextPipeline

from sources.core.manager import RepositoryManager
from sources.pipeline.pipeline_options import PipelineOptions as SourcesOptions

from preprocessing.core.manager import PreprocessingManager
from preprocessing.pipeline.pipeline_options import PipelineOptions as PreprocessingOptions

from generators.execution.integration.pipeline import IntegrationPipeline as ExecutionPipeline
from generators.execution.cli.configuration import build_pipeline_context as build_execution_context

from generators.approval.pipeline import ApprovalPipeline
from generators.approval.cli.configuration import build_pipeline_context as build_approval_context

from generators.conversation.pipeline import ConversationPipeline
from generators.conversation.cli.configuration import (
    build_pipeline_context as build_conversation_context,
)

from generators.evaluation.cli.configuration import Configuration as EvalConfig
from generators.evaluation.cli.commands import Commands as EvalCommands

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("build_dataset")


@dataclass(frozen=True, slots=True)
class DatasetArtifact:
    """Generated dataset artifact registered by the build orchestrator."""

    generator: str
    jsonl_path: Path
    manifest_path: Path | None
    statistics_path: Path | None
    records: tuple[dict[str, Any], ...]


class DatasetArtifactRegistry:
    """Local registry for passing generated datasets between downstream generators."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir
        self._artifacts: dict[str, DatasetArtifact] = {}

    def register(
        self,
        generator: str,
        jsonl_filename: str,
        *,
        manifest_filename: str | None = None,
        statistics_filename: str | None = None,
        required: bool = True,
    ) -> DatasetArtifact | None:
        jsonl_path = self.output_dir / jsonl_filename
        if not jsonl_path.exists():
            if required:
                raise RuntimeError(f"Missing generated dataset for {generator}: {jsonl_path}")
            return None

        records = self._load_jsonl(jsonl_path)
        if required and not records:
            raise RuntimeError(f"Generated dataset for {generator} is empty: {jsonl_path}")

        artifact = DatasetArtifact(
            generator=generator,
            jsonl_path=jsonl_path,
            manifest_path=(self.output_dir / manifest_filename) if manifest_filename else None,
            statistics_path=(self.output_dir / statistics_filename)
            if statistics_filename
            else None,
            records=records,
        )
        self._artifacts[generator] = artifact
        logger.info(
            "Registered %s artifact: %s (%d records)",
            generator,
            jsonl_path,
            len(records),
        )
        return artifact

    def records_for(
        self, *generators: str, optional: tuple[str, ...] = ()
    ) -> MappingProxyType[str, tuple[dict[str, Any], ...]]:
        selected: dict[str, tuple[dict[str, Any], ...]] = {}
        optional_names = set(optional)
        for generator in generators:
            artifact = self._artifacts.get(generator)
            if artifact is None:
                if generator in optional_names:
                    continue
                raise RuntimeError(f"Required upstream artifact is not registered: {generator}")
            if not artifact.records and generator not in optional_names:
                raise RuntimeError(f"Required upstream artifact has no records: {generator}")
            selected[generator] = artifact.records
        return MappingProxyType(selected)

    @staticmethod
    def _load_jsonl(path: Path) -> tuple[dict[str, Any], ...]:
        records: list[dict[str, Any]] = []
        with open(path, encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"Invalid JSONL in {path}:{line_number}: {exc}") from exc
                if not isinstance(record, dict):
                    raise RuntimeError(f"Invalid non-object JSONL record in {path}:{line_number}")
                records.append(record)
        return tuple(records)


def run_generator(name: str, func, *args, **kwargs) -> None:
    """Run a generator pipeline with error handling."""
    logger.info("=" * 60)
    logger.info(f"Starting {name} Generator...")
    logger.info("=" * 60)
    result = func(*args, **kwargs)

    # Some pipelines return a boolean success
    if isinstance(result, bool):
        if not result:
            raise RuntimeError(f"{name} pipeline returned False indicating failure.")

    if not isinstance(result, bool):
        if hasattr(result, "status"):
            from generators.common.pipeline.status import PipelineStatus

            if result.status == PipelineStatus.FAILED:
                diagnostics = getattr(result, "diagnostics", [])
                raise RuntimeError(f"{name} pipeline failed. Diagnostics: {diagnostics}")
            elif result.status == PipelineStatus.SKIPPED:
                logger.info(
                    f"{name} Generator skipped execution (expected without full upstream data)."
                )
            else:
                logger.info(f"{name} Generator completed successfully.")
        elif hasattr(result, "success"):
            if not getattr(result, "success"):
                diagnostics = getattr(result, "diagnostics", [])
                error_msg = f"{name} pipeline failed. Diagnostics: {diagnostics}"
                raise RuntimeError(error_msg)
            logger.info(f"{name} Generator completed successfully.")


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
        logger.warning(
            f"Evaluation configuration not found at {eval_config_path}. Evaluation may fail if required."
        )

    logger.info(f"Initializing AIODOO Dataset build sequence using config: {config_path}")
    logger.info(f"Output directory set to: {output_dir}")

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = DatasetArtifactRegistry(output_dir)

    workers = 4
    resume = False
    reset_checkpoint = True

    # Initialize Sources Framework
    cache_db_path = output_dir / "sources.sqlite"
    repo_manager = RepositoryManager(cache_db_path)

    logger.info("Initializing RepositoryContext via Sources Framework...")
    options = SourcesOptions()
    pipeline_result = repo_manager.load(config_path, options)

    if not pipeline_result.success or pipeline_result.context is None:
        logger.error("Failed to load RepositoryContext.")
        for err in pipeline_result.errors:
            logger.error(f"  - {err}")
        sys.exit(1)

    repository_context = pipeline_result.context
    logger.info(
        f"RepositoryContext loaded successfully. Repositories: {len(repository_context.repositories)}"
    )

    # Initialize Preprocessing Framework
    logger.info("Initializing PreprocessedRepositoryContext via Preprocessing Framework...")
    prep_manager = PreprocessingManager(output_dir / "preprocessing_cache.sqlite")
    prep_result = prep_manager.normalize(repository_context, PreprocessingOptions())

    if not prep_result.success or prep_result.context is None:
        logger.error("Failed to normalize RepositoryContext.")
        logger.error(f"  - {prep_result.error_message}")
        sys.exit(1)

    preprocessed_context = prep_result.context
    logger.info(
        f"PreprocessedRepositoryContext loaded successfully. Cache Hit: {prep_result.statistics.cache_hit}"
    )

    # Initialize Protocol Framework
    logger.info("Assembling ProtocolContext via Protocol Framework...")
    from protocol.core.manager import ProtocolManager
    from protocol.pipeline.assembly_options import AssemblyOptions as ProtocolOptions

    protocol_manager = ProtocolManager()
    protocol_result = protocol_manager.assemble(
        preprocessed_context, ProtocolOptions(validate_schema=True)
    )

    if not protocol_result.validation_result.valid:
        logger.error("Failed to assemble ProtocolContext.")
        for err in protocol_result.validation_result.errors:
            logger.error(f"  - {err}")
        sys.exit(1)

    protocol_context = protocol_result.protocol_context
    if protocol_context is None:
        logger.error("ProtocolContext is None.")
        sys.exit(1)

    logger.info(
        f"ProtocolContext assembled successfully. Objects created: {protocol_result.statistics.objects_created}"
    )

    # 1. Planner
    run_generator(
        "Planner",
        lambda: PlannerPipeline(
            repository_context=preprocessed_context,
            protocol_context=protocol_context,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            reset_checkpoint=reset_checkpoint,
        ).run(),
    )
    artifacts.register(
        "planner",
        "planner_v1_0.jsonl",
        manifest_filename="planner_manifest.json",
        statistics_filename="planner_statistics.json",
    )

    # 2. Coding
    run_generator(
        "Coding",
        lambda: CodingPipeline(
            repository_context=preprocessed_context,
            protocol_context=protocol_context,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            reset_checkpoint=reset_checkpoint,
        ).run(),
    )
    artifacts.register(
        "coding",
        "coding_v1_0.jsonl",
        manifest_filename="coding_manifest.json",
        statistics_filename="coding_statistics.json",
    )

    # 3. Repair
    run_generator(
        "Repair",
        lambda: RepairPipeline(
            repository_context=preprocessed_context,
            protocol_context=protocol_context,
            output_dir=output_dir,
            workers=workers,
            resume=resume,
            reset_checkpoint=reset_checkpoint,
        ).run(),
    )
    artifacts.register(
        "repair",
        "repair_v1_0.jsonl",
        manifest_filename="repair_manifest.json",
        statistics_filename="repair_statistics.json",
    )

    # 4. Context
    run_generator(
        "Context",
        lambda: ContextPipeline(
            repository_context=preprocessed_context,
            protocol_context=protocol_context,
            output_dir=str(output_dir),
            workers=workers,
            resume=resume,
            limit=None,
            target_module=None,
        ).run(),
    )
    artifacts.register(
        "context",
        "context_v1_0.jsonl",
        manifest_filename="manifest.json",
        statistics_filename="statistics.json",
    )

    # Prepare namespace for subsequent generators
    common_ns = argparse.Namespace(
        source_dir=Path("sources"),
        repository_context=preprocessed_context,
        protocol_context=protocol_context,
        output_dir=output_dir,
        debug=False,
        fail_fast=True,
    )

    # 5. Execution
    common_ns.artifact_records = artifacts.records_for(
        "planner", "coding", "context", "repair", optional=("repair",)
    )
    run_generator(
        "Execution",
        lambda: ExecutionPipeline.execute(build_execution_context(common_ns)),
    )
    artifacts.register(
        "execution",
        "execution_dataset.jsonl",
        manifest_filename="execution_manifest.json",
        statistics_filename="execution_statistics.json",
    )

    # 6. Approval
    common_ns.artifact_records = artifacts.records_for("planner", "coding", "repair", "execution")
    run_generator(
        "Approval",
        lambda: ApprovalPipeline.generate(build_approval_context(common_ns)),
    )
    artifacts.register(
        "approval",
        "approval_dataset.jsonl",
        manifest_filename="approval_manifest.json",
        statistics_filename="approval_statistics.json",
    )

    # 7. Conversation (Approval/context/repair are soft dialogue material)
    common_ns.artifact_records = artifacts.records_for(
        "planner",
        "coding",
        "repair",
        "context",
        "execution",
        "approval",
        optional=("repair", "context", "approval"),
    )
    run_generator(
        "Conversation",
        lambda: ConversationPipeline.generate(build_conversation_context(common_ns)),
    )
    artifacts.register(
        "conversation",
        "conversation_dataset.jsonl",
        manifest_filename="conversation_manifest.json",
        statistics_filename="conversation_statistics.json",
    )

    # 8. Evaluation
    eval_config = EvalConfig.load(str(eval_config_path))
    # Inject protocol context dynamically
    eval_config["protocol_context"] = protocol_context
    eval_config["source_protocols"] = artifacts.records_for(
        "planner",
        "coding",
        "repair",
        "context",
        "execution",
        "approval",
        "conversation",
    )
    eval_config["target_generator"] = "aiodoo"
    eval_config["benchmark_name"] = "aiodoo_downstream_integration"
    eval_config["benchmark_category"] = "integration"
    eval_config["benchmark_description"] = "Evaluation generated from all AIODOO datasets."
    eval_config["supported_protocols"] = tuple(eval_config["source_protocols"].keys())

    run_generator(
        "Evaluation",
        lambda: EvalCommands.run_generate(eval_config, str(output_dir)),
    )
    artifacts.register(
        "evaluation",
        "evaluation_dataset.jsonl",
        manifest_filename="evaluation_manifest.json",
        statistics_filename="evaluation_statistics.json",
    )

    # 8b. Per-capability evaluation corpora, built from the canonical
    # aiodoo_contract schemas (ACT-007 / DEF-05 — see MASTER_ACTION_LIST.md
    # and ARCHITECTURE_FREEZE_REPORT.md Tier 1). This is distinct from the
    # "Evaluation" generator above: that generator produces one aggregate,
    # cross-capability integration benchmark; this step produces one
    # contract-shaped (request, expected_response) gold corpus per learnable
    # capability for aiodoo-validation to certify against.
    logger.info("=" * 60)
    logger.info("Building per-capability evaluation corpora (aiodoo_contract)...")
    logger.info("=" * 60)

    from generators.common.contract.adapters import SUPPORTED_CAPABILITIES
    from generators.common.contract.eval_corpus import write_eval_corpus

    eval_corpus_source_records = artifacts.records_for(*SUPPORTED_CAPABILITIES)
    for capability in SUPPORTED_CAPABILITIES:
        eval_report = write_eval_corpus(
            capability, eval_corpus_source_records[capability], output_dir
        )
        logger.info(
            "%s eval corpus: %d candidate(s) -> %d written "
            "(%d skipped: not projectable, %d skipped: failed contract validation)",
            capability,
            eval_report.candidates,
            eval_report.written,
            eval_report.skipped_projection,
            eval_report.skipped_validation,
        )
        if eval_report.written == 0:
            raise RuntimeError(
                f"Eval corpus generation produced zero contract-valid cases for "
                f"capability '{capability}'."
            )

    # 9. Validation Framework
    logger.info("=" * 60)
    logger.info("Starting Validation Framework...")
    logger.info("=" * 60)

    from validation.core.manager import ValidationManager
    from validation.pipeline.pipeline_options import ValidationOptions
    from validation.domain.enums import ReportFormat
    from validation.reports.console_reporter import ConsoleReporter

    val_manager = ValidationManager()
    val_result = val_manager.validate(
        dataset_dir=output_dir,
        options=ValidationOptions(
            fail_fast=False,
            parallel=False,
            workers=workers,
            report_format=ReportFormat.CONSOLE,
        ),
        protocol_context=protocol_context,
    )

    ConsoleReporter().report(val_result.report, output_dir)

    if not val_result.success:
        logger.error("Validation FAILED. See report above for details.")
        sys.exit(2)

    logger.info("=" * 60)
    logger.info("All pipelines executed and validated successfully.")
    logger.info(f"Final datasets are available in: {output_dir}")
    logger.info("=" * 60)
    sys.exit(0)


if __name__ == "__main__":
    main()
