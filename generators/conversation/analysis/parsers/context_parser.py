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
        for doc in data.get("documents", []):
            references.append(
                Reference(
                    source_generator="context",
                    source_reference=doc.get("doc_id", "unknown"),
                    description=f"Context document: {doc.get('title', '')}",
                )
            )
        return ExtractedEvidence(
            protocol_name="context_protocol",
            references=tuple(references),
            attachments=(),
            raw_data=MappingProxyType(data),
        )
