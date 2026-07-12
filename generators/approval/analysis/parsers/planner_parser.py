"""Planner parser for the Approval Generator."""

from typing import Any, List
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.source_generator import SourceGenerator
from generators.approval.analysis.parsers.base_parser import BaseParser
from generators.approval.analysis.parsers.parser_registry import ParserRegistry


@ParserRegistry.register("planner_data")
class PlannerParser(BaseParser):  # type: ignore[misc]
    """Parses Planner protocol data to extract evidence."""

    def parse(self, data: Any) -> List[Evidence]:
        evidence_list = []  # type: ignore[var-annotated]
        if not data:
            return evidence_list

        import hashlib

        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            output = record.get("output", {})
            tasks = output.get("tasks", []) if isinstance(output, dict) else []
            if not tasks:
                tasks = record.get("tasks", [])
            record_ref = record.get("metadata", {}).get("protocol_hash", "planner")

            for task in tasks:
                if not isinstance(task, dict):
                    continue
                source_ref = f"{record_ref}:{task.get('id', 'unknown_task')}"
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
