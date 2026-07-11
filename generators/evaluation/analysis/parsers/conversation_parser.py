"""Conversation Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class ConversationParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Conversation protocol objects."""

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract conversational turns and interaction dynamics."""
        # Simulated read-only extraction
        return {
            "source_type": "conversation",
            "raw_data": getattr(protocol_object, "model_dump", lambda: {})(),
        }


ParserRegistry.register("conversation", ConversationParser)
