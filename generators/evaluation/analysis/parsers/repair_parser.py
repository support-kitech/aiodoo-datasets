"""Repair Parser for Evaluation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.evaluation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry


class RepairParser(BaseParser):
    """Extracts deterministic evidence from Repair protocol objects."""

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract repair patches and error traces."""
        # Simulated read-only extraction
        return {
            "source_type": "repair",
            "raw_data": getattr(protocol_object, "model_dump", lambda: {})(),
        }


ParserRegistry.register("repair", RepairParser)
