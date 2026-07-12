"""Coding Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class CodingParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Coding protocol objects."""

    source_type = "coding"

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract code snippets and AST structures."""
        return self._aggregate_records(protocol_object)


ParserRegistry.register("coding", CodingParser)
