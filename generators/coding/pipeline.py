"""The ETL Pipeline Orchestrator for the Coding Dataset Generator."""

import logging
from pathlib import Path

from preprocessing.domain.repository import PreprocessedModule
from generators.coding.discovery import (
    OdooASTParser,
    OdooXMLParser,
    ScenarioClassifier,
)
from generators.coding.generation.instruction import generate_instruction
from generators.coding.generation.context_builder import build_context
from generators.coding.generation.artifact_builder import build_artifacts
from generators.coding.protocol.mapper import build_artifact_payload
from generators.coding.validation.schema import CodingDatasetRecord, ArtifactPayload
from generators.common.validation.deduplicator import Deduplicator
from generators.coding.validation.core_validator import CoreProtocolValidator
from generators.coding.export.metadata import build_metadata, compute_protocol_hash
from generators.common.export.writer import DatasetWriter
from generators.common.state.checkpoint import CheckpointManager
from generators.coding.statistics.coding_statistics import CodingStatistics
from generators.common.pipeline.orchestrator import SharedPipelineOrchestrator

logger = logging.getLogger(__name__)


def run_discovery(module: PreprocessedModule):  # type: ignore[no-untyped-def]
    """Stage 1: Discovery"""
    ast_parser = OdooASTParser()
    xml_parser = OdooXMLParser()
    module_path = Path(str(module.metadata["path"]))
    py_k = ast_parser.parse_module(module_path)
    xml_k = xml_parser.parse_module(module_path)
    return py_k, xml_k


def run_classification(module: PreprocessedModule, py_k, xml_k):  # type: ignore[no-untyped-def]
    """Stage 2: Classification"""
    classifier = ScenarioClassifier()
    return classifier.classify(module, py_k, xml_k)


def run_context(module: PreprocessedModule, scenario, py_k, xml_k, artifacts):  # type: ignore[no-untyped-def]
    """Stage 3: Context"""
    dummy_payload = ArtifactPayload(
        goal="", workspace="", artifacts=artifacts, operations=[], validation_actions=[], summary=""
    )
    return build_context(module, scenario, py_k, xml_k, dummy_payload)


def run_instruction(module: PreprocessedModule, scenario, context):  # type: ignore[no-untyped-def]
    """Stage 4: Instruction"""
    base = generate_instruction(module, scenario)

    models = context.get("existing_models", [])
    if models:
        base += f"\nContext: Models available -> {', '.join(models)}."
    return base


def run_protocol_mapping(module: PreprocessedModule, scenario, py_k, xml_k, artifacts):  # type: ignore[no-untyped-def]
    """Stage 5 & 6: Artifact & Protocol Mapping"""
    return build_artifact_payload(module, scenario, py_k, xml_k, artifacts)


def run_metadata(module: PreprocessedModule, scenario, protocol_hash: str):  # type: ignore[no-untyped-def]
    """Stage 7: Export Metadata"""
    return build_metadata(module, scenario, protocol_hash)


def compute_record_hash(module: PreprocessedModule, scenario, payload):  # type: ignore[no-untyped-def]
    """Compute a per-record protocol hash from the payload."""
    return compute_protocol_hash(module, scenario, payload)


def process_module(module: PreprocessedModule, protocol_hash: str) -> list[dict]:  # type: ignore[type-arg]
    """Worker function orchestrating the strictly ordered pipeline stages."""
    try:
        py_k, xml_k = run_discovery(module)
        scenarios = run_classification(module, py_k, xml_k)

        results = []
        for scenario in scenarios:
            artifacts = build_artifacts(module, scenario, py_k, xml_k)
            context = run_context(module, scenario, py_k, xml_k, artifacts)
            instruction = run_instruction(module, scenario, context)
            payload = run_protocol_mapping(module, scenario, py_k, xml_k, artifacts)
            record_hash = compute_record_hash(module, scenario, payload)
            metadata = run_metadata(module, scenario, record_hash)

            results.append(
                {
                    "instruction": instruction,
                    "context": context,
                    "output": payload.model_dump(),
                    "metadata": metadata,
                }
            )

        return results
    except Exception as exc:
        logger.error("Error processing module %s: %s", module.name, exc)
        return []


class CodingPipeline(SharedPipelineOrchestrator):  # type: ignore[misc]
    """Orchestrates the deterministic generation of Artifact Protocol V1 JSONL."""

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
            stats=CodingStatistics(),
            filename="coding_v1_0.jsonl",
            dataset_name="AIODOO Coding Dataset",
        )
        deduplicator = Deduplicator()
        core_validator = CoreProtocolValidator()
        checkpoint = CheckpointManager(output_dir=output_dir, filename="coding_checkpoint.json")

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
            record_class=CodingDatasetRecord,
            validation_method="validate_payload",
            checkpoint_strategy="artifact",
            stats_filename="coding_statistics.json",
            manifest_filename="coding_manifest.json",
            workers=workers,
            resume=resume,
        )
