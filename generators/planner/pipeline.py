"""The ETL Pipeline Orchestrator for the Planner Dataset Generator."""

import logging
from pathlib import Path

from preprocessing.domain.repository import PreprocessedModule
from generators.common.discovery import (
    OdooASTParser,
    OdooXMLParser,
    ScenarioClassifier,
)

from generators.planner.synthetics.instruction import generate_instruction
from generators.planner.synthetics.context_builder import build_context
from generators.planner.protocol.mapper import build_plan_payload
from generators.planner.validation.schema import PlannerDatasetRecord
from generators.common.validation.deduplicator import Deduplicator
from generators.planner.validation.core_validator import CoreProtocolValidator
from generators.planner.export.metadata import build_metadata, compute_protocol_hash
from generators.common.export.writer import DatasetWriter
from generators.common.state.checkpoint import CheckpointManager
from generators.planner.statistics.planner_statistics import PlannerStatistics
from generators.common.pipeline.orchestrator import SharedPipelineOrchestrator

logger = logging.getLogger(__name__)


def process_module(module: PreprocessedModule, protocol_hash: str) -> list[dict]:  # type: ignore[type-arg]
    """Worker function to process a single module independently."""
    try:
        ast_parser = OdooASTParser()
        xml_parser = OdooXMLParser()
        classifier = ScenarioClassifier()

        py_k = ast_parser.parse_module(Path(str(module.metadata["path"])))
        xml_k = xml_parser.parse_module(Path(str(module.metadata["path"])))
        scenarios = classifier.classify(module, py_k, xml_k)

        results = []
        for scenario in scenarios:
            instruction = generate_instruction(module, scenario)
            context = build_context(module)
            payload = build_plan_payload(module, scenario, py_k, xml_k)
            record_hash = compute_protocol_hash(module, scenario, payload)
            metadata = build_metadata(module, scenario, record_hash)

            results.append(
                {
                    "instruction": instruction,
                    "input": context,
                    "output": payload.model_dump(),  # We serialize here for transport back to main process
                    "metadata": metadata,
                }
            )

        return results
    except KeyError as exc:
        logger.error("Error processing module %s. Missing key %s in metadata: %s", module.name, exc, module.metadata)
        return []
    except Exception as exc:
        logger.error("Error processing module %s: %s", module.name, exc)
        return []


class PlannerPipeline(SharedPipelineOrchestrator):  # type: ignore[misc]
    """Orchestrates the deterministic generation of Protocol V1 JSONL."""

    def __init__(
        self,
        repository_context,
        protocol_context,
        output_dir: Path,
        workers: int = 4,
        resume: bool = False,
        reset_checkpoint: bool = False,
    ) -> None:
        self.protocol_context = protocol_context
        writer = DatasetWriter(
            output_dir=output_dir,
            stats=PlannerStatistics(),
            filename="planner_v1_0.jsonl",
            dataset_name="AIODOO Planner Dataset",
        )
        deduplicator = Deduplicator()
        core_validator = CoreProtocolValidator()
        checkpoint = CheckpointManager(output_dir=output_dir, filename="planner_checkpoint.json")

        if reset_checkpoint:
            checkpoint.clear()
        if resume:
            checkpoint.load()

        import functools
        worker_fn = functools.partial(process_module, protocol_hash="unused")

        super().__init__(
            repository_context=repository_context,
            writer=writer,
            deduplicator=deduplicator,
            core_validator=core_validator,
            checkpoint=checkpoint,
            worker_fn=worker_fn,
            record_class=PlannerDatasetRecord,
            validation_method="validate_plan",
            checkpoint_strategy="module",
            stats_filename="planner_statistics.json",
            manifest_filename="planner_manifest.json",
            workers=workers,
            resume=resume,
        )
