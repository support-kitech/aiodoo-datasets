"""Coding Parser for Evaluation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.evaluation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry

class CodingParser(BaseParser):
    """Extracts deterministic evidence from Coding protocol objects."""
    
    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract code snippets and AST structures."""
        # Simulated read-only extraction
        return {"source_type": "coding", "raw_data": getattr(protocol_object, "model_dump", lambda: {})()}

ParserRegistry.register("coding", CodingParser)
