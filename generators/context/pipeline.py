"""Orchestrates the Context Dataset execution pipeline."""

import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from generators.common.discovery.scanner import ModuleScanner, OdooModule
from generators.common.discovery.ast_parser import OdooASTParser
from generators.common.discovery.xml_parser import OdooXMLParser
from generators.common.validation.deduplicator import Deduplicator
from generators.context.analysis.knowledge import ContextKnowledge
from generators.context.analysis.graph.graph import ContextGraph
from generators.context.analysis.graph_builder import GraphBuilder
from generators.context.generation.query_generator import QueryGenerator
from generators.context.ranking.ranking_engine import RankingEngine
from generators.context.protocol.mapper import ContextMapper
from generators.context.validation.registry import REGISTERED_VALIDATORS
from generators.context.statistics.context_statistics import ContextStatistics
from generators.context.state.checkpoint import CheckpointManager
from generators.context.export.writer import DatasetWriter
from generators.context.protocol.schema import ContextTask

logger = logging.getLogger(__name__)


def process_module(module: OdooModule) -> list[ContextTask]:
    """Worker function to process a single module and return a list of Protocol tasks."""
    try:
        # Discovery
        ast_parser = OdooASTParser()
        xml_parser = OdooXMLParser()

        py_knowledge = ast_parser.parse_module(module.path)
        xml_knowledge = xml_parser.parse_module(module.path)

        # We need to construct ContextKnowledge correctly
        manifest_dict = {}
        if module.manifest:
            manifest_dict = {"depends": module.manifest.depends, "data": module.manifest.data}

        security_dict = {}
        if hasattr(xml_knowledge, "files"):
            for path, k in xml_knowledge.files.items():
                if k.security_rules:
                    security_dict[path] = k.security_rules

        knowledge = ContextKnowledge(
            module_name=module.name,
            python_files=py_knowledge.files if hasattr(py_knowledge, "files") else {},
            xml_files=xml_knowledge.files if hasattr(xml_knowledge, "files") else {},
            manifest=manifest_dict,
            security=security_dict,
        )

        # Graph
        graph = ContextGraph()

        # Populate nodes from ContextKnowledge
        from generators.context.analysis.graph.graph import ContextNode
        from generators.context.analysis.graph.enums import NodeType, LanguageType

        for file_path, k in knowledge.python_files.items():
            for model_name, model_def in k.models.items():
                graph.add_node(
                    ContextNode(
                        name=model_name,
                        module=module.name,
                        relative_path=file_path,
                        node_type=NodeType.MODEL,
                        language=LanguageType.PYTHON,
                    )
                )
                for field_name, field_def in model_def.fields.items():
                    graph.add_node(
                        ContextNode(
                            name=field_name,
                            module=module.name,
                            relative_path=file_path,
                            node_type=NodeType.FIELD,
                            language=LanguageType.PYTHON,
                        )
                    )

        for file_path, k in knowledge.xml_files.items():
            for view in k.views:
                graph.add_node(
                    ContextNode(
                        name=view.id,
                        module=module.name,
                        relative_path=file_path,
                        node_type=NodeType.VIEW,
                        language=LanguageType.XML,
                    )
                )

        builder = GraphBuilder()
        builder.build_relationships(graph, knowledge)

        # Query
        generator = QueryGenerator()
        queries = generator.generate_queries(graph)

        # Ranking
        engine = RankingEngine()
        mapper = ContextMapper()

        tasks = []
        for query in queries:
            results = engine.rank(query, graph)
            if results:
                try:
                    task = mapper.map(query, results, graph)
                    tasks.append(task)
                except Exception:
                    # Logging already handled inside mapper
                    pass

        return tasks
    except Exception as e:
        logger.exception("Module %s failed processing: %s", module.name, e)
        return []


class ContextPipeline:
    """Orchestrates the generation of the Context Protocol dataset."""

    def __init__(
        self,
        config_path: str,
        output_dir: str,
        workers: int = 4,
        resume: bool = False,
        limit: int | None = None,
        target_module: str | None = None,
    ) -> None:
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.workers = workers
        self.resume = resume
        self.limit = limit
        self.target_module = target_module

        self.scanner = ModuleScanner(self.config_path, self.output_dir / "cache")
        self.checkpoint = CheckpointManager(self.output_dir)
        self.stats = ContextStatistics()
        self.writer = DatasetWriter(
            self.output_dir, self.stats, "context_v1_0.jsonl", "aiodoo_context"
        )
        self.deduplicator = Deduplicator()

        self.validators = [v() for v in REGISTERED_VALIDATORS]

    def run(self) -> None:
        """Executes the complete generation pipeline."""
        logger.info("Initializing Context Pipeline...")
        all_modules = self.scanner.discover_modules()
        logger.info("Discovered %d modules.", len(all_modules))

        if self.target_module:
            all_modules = [m for m in all_modules if m.name == self.target_module]
            logger.info("Filtered to module: %s", self.target_module)

        if self.resume:
            self.checkpoint.load()
            modules_to_process = [
                m for m in all_modules if not self.checkpoint.is_module_fully_processed(m.name)
            ]
            logger.info(
                "Resuming. Processing %d out of %d modules.",
                len(modules_to_process),
                len(all_modules),
            )
        else:
            self.checkpoint.clear()
            modules_to_process = all_modules

        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            future_to_module = {
                executor.submit(process_module, mod): mod for mod in modules_to_process
            }

            for future in as_completed(future_to_module):
                mod = future_to_module[future]
                try:
                    tasks = future.result()
                    for task in tasks:
                        # Deduplication using task.id
                        if not self.deduplicator.is_unique(task.id):
                            self.writer.record_duplicate()
                            continue

                        # Incremental generation / resume check at artifact level
                        if self.resume and self.checkpoint.is_processed(
                            "odoo", mod.name, "context_task", task.id
                        ):
                            continue

                        # Validation
                        is_valid = True
                        for validator in self.validators:
                            result = validator.validate(task)
                            if not result.valid:
                                is_valid = False
                                break

                        if not is_valid:
                            self.writer.record_validation_failure()
                            continue

                        # Write & Checkpoint
                        self.writer.write_record(task)
                        self.checkpoint.save(
                            "odoo", mod.name, "context_task", task.id, self.writer.written_count
                        )

                        if self.limit and self.writer.written_count >= self.limit:
                            logger.info("Generation limit reached: %d", self.limit)
                            break

                    # Mark module as processed (we save a dummy hash to denote module completion in legacy terms)
                    self.checkpoint.save(
                        "odoo", mod.name, "module_completion", "done", self.writer.written_count
                    )
                    self.scanner.update_cache(mod)

                    if self.limit and self.writer.written_count >= self.limit:
                        break

                except Exception as e:
                    logger.error("Failed executing module %s: %s", mod.name, e)

        self.writer.export_statistics("statistics.json")
        self.writer.export_manifest("manifest.json")
        logger.info("Context Pipeline complete. Wrote %d records.", self.writer.written_count)
