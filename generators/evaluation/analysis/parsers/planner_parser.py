"""Planner Parser for Evaluation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.evaluation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry

class PlannerParser(BaseParser):
    """Extracts deterministic evidence from Planner protocol objects."""
    
    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract planner instructions and structure."""
        # Simulated read-only extraction
        return {"source_type": "planner", "raw_data": getattr(protocol_object, "model_dump", lambda: {})()}

# Statically register parser
ParserRegistry.register("planner", PlannerParser)
