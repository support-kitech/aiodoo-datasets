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
        for task in data.get("tasks", []):
            references.append(
                Reference(
                    source_generator="planner",
                    source_reference=task.get("task_id", "unknown"),
                    description=f"Planner task: {task.get('description', '')}",
                )
            )
        return ExtractedEvidence(
            protocol_name="planner_protocol",
            references=tuple(references),
            attachments=(),
            raw_data=MappingProxyType(data),
        )
