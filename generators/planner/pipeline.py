"""The ETL Pipeline Orchestrator for the Planner Dataset Generator."""

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Sequence

from aiodoo_datasets.generators.planner.discovery import ModuleScanner, OdooModule, OdooASTParser, OdooXMLParser, ScenarioClassifier

from aiodoo_datasets.generators.planner.synthetics.instruction import generate_instruction
from aiodoo_datasets.generators.planner.synthetics.context_builder import build_context
from aiodoo_datasets.generators.planner.protocol.mapper import build_plan_payload
from aiodoo_datasets.generators.planner.validation.schema import PlannerDatasetRecord
from aiodoo_datasets.generators.common.validation.deduplicator import Deduplicator
from aiodoo_datasets.generators.planner.validation.core_validator import CoreProtocolValidator
from aiodoo_datasets.generators.planner.export.metadata import build_metadata
from aiodoo_datasets.generators.common.export.writer import DatasetWriter
from aiodoo_datasets.generators.common.state.checkpoint import CheckpointManager
from aiodoo_datasets.generators.planner.statistics.planner_statistics import PlannerStatistics

logger = logging.getLogger(__name__)

def process_module(module: OdooModule) -> list[dict]:
    """Worker function to process a single module independently."""
    try:
        ast_parser = OdooASTParser()
        xml_parser = OdooXMLParser()
        classifier = ScenarioClassifier()
        
        py_k = ast_parser.parse_module(module.path)
        xml_k = xml_parser.parse_module(module.path)
        scenarios = classifier.classify(module, py_k, xml_k)
        
        results = []
        for scenario in scenarios:
            instruction = generate_instruction(module, scenario)
            context = build_context(module)
            payload = build_plan_payload(module, scenario, py_k, xml_k)
            metadata = build_metadata(module, scenario, payload)
            
            results.append({
                "instruction": instruction,
                "input": context,
                "output": payload.model_dump(),  # We serialize here for transport back to main process
                "metadata": metadata
            })
            
        return results
    except Exception as exc:
        logger.error("Error processing module %s: %s", module.name, exc)
        return []


from aiodoo_datasets.generators.common.pipeline.orchestrator import SharedPipelineOrchestrator

class PlannerPipeline(SharedPipelineOrchestrator):
    """Orchestrates the deterministic generation of Protocol V1 JSONL."""

    def __init__(self, sources_yaml: Path, output_dir: Path, workers: int = 4, resume: bool = False, reset_checkpoint: bool = False):
        scanner = ModuleScanner(config_path=sources_yaml, cache_dir=output_dir / "cache")
        writer = DatasetWriter(
            output_dir=output_dir,
            stats=PlannerStatistics(),
            filename="planner_v1_0.jsonl",
            dataset_name="AIODOO Planner Dataset"
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
            record_class=PlannerDatasetRecord,
            validation_method="validate_plan",
            checkpoint_strategy="module",
            stats_filename="planner_statistics.json",
            manifest_filename="planner_manifest.json",
            workers=workers,
            resume=resume
        )
