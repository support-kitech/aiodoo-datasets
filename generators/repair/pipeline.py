"""The ETL Pipeline Orchestrator for the Repair Dataset Generator."""

import logging
from pathlib import Path

from generators.common.discovery.scanner import ContextModuleScanner, OdooModule
from generators.repair.analysis.analyzer import RepairAnalyzer
from generators.repair.generation.instruction import generate_instruction
from generators.repair.protocol.mapper import build_repair_payload
from generators.repair.validation.schema import RepairDatasetRecord
from generators.common.validation.deduplicator import Deduplicator
from generators.repair.validation.core_validator import CoreProtocolValidator
from generators.repair.export.metadata import build_metadata
from generators.common.export.writer import DatasetWriter
from generators.common.state.checkpoint import CheckpointManager
from generators.repair.statistics.repair_statistics import RepairStatistics
from generators.common.pipeline.orchestrator import SharedPipelineOrchestrator

logger = logging.getLogger(__name__)


def process_module(module: OdooModule) -> list[dict]:  # type: ignore[type-arg]
    """Worker function orchestrating the strictly ordered pipeline stages."""
    try:
        analyzer = RepairAnalyzer()
        opportunities = analyzer.analyze(module)

        if not opportunities:
            return []

        instruction = generate_instruction(module, opportunities)
        payload = build_repair_payload(module, opportunities)
        metadata = build_metadata(module, payload)

        return [
            {
                "instruction": instruction,
                "context": {"module_name": module.name},
                "output": payload.model_dump(),
                "metadata": metadata,
            }
        ]
    except Exception as exc:
        logger.error("Error processing module %s: %s", module.name, exc)
        return []


class RepairPipeline(SharedPipelineOrchestrator):  # type: ignore[misc]
    """Orchestrates the deterministic generation of Repair Protocol V1 JSONL."""

    def __init__(
        self,
        repository_context,
        output_dir: Path,
        workers: int = 4,
        resume: bool = False,
        reset_checkpoint: bool = False,
    ) -> None:
        scanner = ContextModuleScanner(repository_context)
        stats = RepairStatistics()
        writer = DatasetWriter(
            output_dir=output_dir,
            stats=stats,
            filename="repair_v1_0.jsonl",
            dataset_name="AIODOO Repair Dataset",
        )
        deduplicator = Deduplicator()
        core_validator = CoreProtocolValidator()
        checkpoint = CheckpointManager(output_dir=output_dir)

        if reset_checkpoint:
            checkpoint.clear()
        if resume:
            checkpoint.load()

        super().__init__(
            scanner=scanner,
            writer=writer,
            deduplicator=deduplicator,
            core_validator=core_validator,
            checkpoint=checkpoint,
            worker_fn=process_module,
            record_class=RepairDatasetRecord,
            validation_method="validate_payload",
            checkpoint_strategy="module",
            stats_filename="repair_statistics.json",
            manifest_filename="repair_manifest.json",
            workers=workers,
            resume=resume,
        )
