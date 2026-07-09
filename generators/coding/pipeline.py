"""The ETL Pipeline Orchestrator for the Coding Dataset Generator."""

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from aiodoo_datasets.generators.coding.discovery import ModuleScanner, OdooModule, OdooASTParser, OdooXMLParser, ScenarioClassifier
from aiodoo_datasets.generators.coding.generation.instruction import generate_instruction
from aiodoo_datasets.generators.coding.generation.context_builder import build_context
from aiodoo_datasets.generators.coding.generation.artifact_builder import build_artifacts
from aiodoo_datasets.generators.coding.protocol.mapper import build_artifact_payload
from aiodoo_datasets.generators.coding.validation.schema import CodingDatasetRecord, ArtifactPayload
from aiodoo_datasets.generators.common.validation.deduplicator import Deduplicator
from aiodoo_datasets.generators.coding.validation.core_validator import CoreProtocolValidator
from aiodoo_datasets.generators.coding.export.metadata import build_metadata
from aiodoo_datasets.generators.common.export.writer import DatasetWriter
from aiodoo_datasets.generators.common.state.checkpoint import CheckpointManager
from aiodoo_datasets.generators.coding.statistics.coding_statistics import CodingStatistics

logger = logging.getLogger(__name__)

def run_discovery(module: OdooModule):
    """Stage 1: Discovery"""
    ast_parser = OdooASTParser()
    xml_parser = OdooXMLParser()
    py_k = ast_parser.parse_module(module.path)
    xml_k = xml_parser.parse_module(module.path)
    return py_k, xml_k

def run_classification(module: OdooModule, py_k, xml_k):
    """Stage 2: Classification"""
    classifier = ScenarioClassifier()
    return classifier.classify(module, py_k, xml_k)

def run_context(module: OdooModule, scenario, py_k, xml_k, artifacts):
    """Stage 3: Context"""
    dummy_payload = ArtifactPayload(goal="", workspace="", artifacts=artifacts, operations=[], validation_actions=[], summary="")
    return build_context(module, scenario, py_k, xml_k, dummy_payload)

def run_instruction(module: OdooModule, scenario, context):
    """Stage 4: Instruction"""
    base = generate_instruction(module, scenario)
    
    models = context.get("existing_models", [])
    if models:
        base += f"\nContext: Models available -> {', '.join(models)}."
    return base

def run_protocol_mapping(module: OdooModule, scenario, py_k, xml_k, artifacts):
    """Stage 5 & 6: Artifact & Protocol Mapping"""
    return build_artifact_payload(module, scenario, py_k, xml_k, artifacts)

def run_metadata(module: OdooModule, scenario, payload):
    """Stage 7: Export Metadata"""
    return build_metadata(module, scenario, payload)

def process_module(module: OdooModule) -> list[dict]:
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
            metadata = run_metadata(module, scenario, payload)
            
            results.append({
                "instruction": instruction,
                "context": context,
                "output": payload.model_dump(),
                "metadata": metadata
            })
            
        return results
    except Exception as exc:
        logger.error("Error processing module %s: %s", module.name, exc)
        return []


from aiodoo_datasets.generators.common.pipeline.orchestrator import SharedPipelineOrchestrator

class CodingPipeline(SharedPipelineOrchestrator):
    """Orchestrates the deterministic generation of Artifact Protocol V1 JSONL."""

    def __init__(self, sources_yaml: Path, output_dir: Path, workers: int = 4, resume: bool = False, reset_checkpoint: bool = False):
        scanner = ModuleScanner(config_path=sources_yaml, cache_dir=output_dir / "cache")
        writer = DatasetWriter(
            output_dir=output_dir,
            stats=CodingStatistics(),
            filename="coding_v1_0.jsonl",
            dataset_name="AIODOO Coding Dataset"
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
            record_class=CodingDatasetRecord,
            validation_method="validate_payload",
            checkpoint_strategy="artifact",
            stats_filename="coding_statistics.json",
            manifest_filename="coding_manifest.json",
            workers=workers,
            resume=resume
        )
