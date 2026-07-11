"""Planner parser for the Approval Generator."""

from typing import Dict, Any, List
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
from aiodoo_datasets.generators.approval.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.approval.analysis.parsers.parser_registry import ParserRegistry


@ParserRegistry.register("planner_data")
class PlannerParser(BaseParser):
    """Parses Planner protocol data to extract evidence."""

    def parse(self, data: Dict[str, Any]) -> List[Evidence]:
        evidence_list = []
        if not data:
            return evidence_list

        # Example: extract planned tasks
        tasks = data.get("tasks", [])
        import hashlib

        for task in tasks:
            source_ref = task.get("id", "unknown_task")
            hash_input = f"PLANNER:{source_ref}"
            evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

            evidence_list.append(
                Evidence(
                    evidence_id=f"EVID-{evid_hash}",
                    source_generator=SourceGenerator.PLANNER,
                    source_reference=source_ref,
                    file_path=None,
                    snippet="",
                    description=f"Planner task: {task.get('description', '')}",
                )
            )
        return evidence_list
