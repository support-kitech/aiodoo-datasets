"""Planner parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from aiodoo_datasets.generators.conversation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.conversation.registries.parser_registry import ParserRegistry
from aiodoo_datasets.generators.conversation.analysis.result import ExtractedEvidence
from aiodoo_datasets.generators.conversation.domain.reference import Reference


@ParserRegistry.register("planner_protocol")
class PlannerParser(BaseParser):
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
