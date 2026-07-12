"""Context parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference


@ParserRegistry.register("context_protocol")
class ContextParser(BaseParser):  # type: ignore[misc]
    """Parses Context protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records[:25]:
            if not isinstance(record, dict):
                continue
            query = record.get("query", {})
            query_text = query.get("natural_language", "") if isinstance(query, dict) else ""
            references.append(
                Reference(
                    source_generator="context",
                    source_reference=record.get("id", "unknown"),
                    description=f"Context query: {query_text}",
                )
            )
        return ExtractedEvidence(
            protocol_name="context_protocol",
            references=tuple(references),
            attachments=(),
            raw_data=MappingProxyType({"record_count": len(records)}),
        )
