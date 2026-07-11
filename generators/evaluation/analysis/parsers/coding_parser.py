"""Coding Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class CodingParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Coding protocol objects."""

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract code snippets and AST structures."""
        # Simulated read-only extraction
        return {
            "source_type": "coding",
            "raw_data": getattr(protocol_object, "model_dump", lambda: {})(),
        }


ParserRegistry.register("coding", CodingParser)
