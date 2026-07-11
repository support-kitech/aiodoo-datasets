"""Execution Parser for Evaluation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.evaluation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry


class ExecutionParser(BaseParser):
    """Extracts deterministic evidence from Execution protocol objects."""

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract execution output and environment context."""
        # Simulated read-only extraction
        return {
            "source_type": "execution",
            "raw_data": getattr(protocol_object, "model_dump", lambda: {})(),
        }


ParserRegistry.register("execution", ExecutionParser)
