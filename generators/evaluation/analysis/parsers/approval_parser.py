"""Approval Parser for Evaluation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.evaluation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry


class ApprovalParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Approval protocol objects."""

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract review feedback and verification metadata."""
        # Simulated read-only extraction
        return {
            "source_type": "approval",
            "raw_data": getattr(protocol_object, "model_dump", lambda: {})(),
        }


ParserRegistry.register("approval", ApprovalParser)
