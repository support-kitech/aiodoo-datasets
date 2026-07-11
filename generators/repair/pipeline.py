"""The ETL Pipeline Orchestrator for the Repair Dataset Generator."""

import logging
from pathlib import Path

from aiodoo_datasets.generators.common.discovery.scanner import ModuleScanner, OdooModule
from aiodoo_datasets.generators.repair.analysis.analyzer import RepairAnalyzer
from aiodoo_datasets.generators.repair.generation.instruction import generate_instruction
from aiodoo_datasets.generators.repair.protocol.mapper import build_repair_payload
from aiodoo_datasets.generators.repair.validation.schema import RepairDatasetRecord
from aiodoo_datasets.generators.common.validation.deduplicator import Deduplicator
from aiodoo_datasets.generators.repair.validation.core_validator import CoreProtocolValidator
from aiodoo_datasets.generators.repair.export.metadata import build_metadata
from aiodoo_datasets.generators.common.export.writer import DatasetWriter
from aiodoo_datasets.generators.common.state.checkpoint import CheckpointManager
from aiodoo_datasets.generators.repair.statistics.repair_statistics import RepairStatistics
from aiodoo_datasets.generators.common.pipeline.orchestrator import SharedPipelineOrchestrator

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
        sources_yaml: Path,
        output_dir: Path,
        workers: int = 4,
        resume: bool = False,
        reset_checkpoint: bool = False,
    ) -> None:
        scanner = ModuleScanner(config_path=sources_yaml, cache_dir=output_dir / "cache")
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
