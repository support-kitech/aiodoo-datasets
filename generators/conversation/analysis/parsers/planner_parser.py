"""Planner parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference


@ParserRegistry.register("planner_protocol")
class PlannerParser(BaseParser):  # type: ignore[misc]
    """Parses Planner protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            output = record.get("output", {})
            tasks = output.get("tasks", []) if isinstance(output, dict) else []
            record_ref = record.get("metadata", {}).get("protocol_hash", "planner")
            for task in tasks:
                if not isinstance(task, dict):
                    continue
                references.append(
                    Reference(
                        source_generator="planner",
                        source_reference=f"{record_ref}:{task.get('id', 'unknown')}",
                        description=f"Planner task: {task.get('description', '')}",
                    )
                )
                if len(references) >= 25:
                    break
            if len(references) >= 25:
                break
        return ExtractedEvidence(
            protocol_name="planner_protocol",
            references=tuple(references),
            attachments=(),
            raw_data=MappingProxyType({"record_count": len(records)}),
        )
