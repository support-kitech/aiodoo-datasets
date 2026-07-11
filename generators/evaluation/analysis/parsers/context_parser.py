"""Context Parser for Evaluation Generator."""

from typing import Dict, Any
from aiodoo_datasets.generators.evaluation.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry


class ContextParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Context protocol objects."""

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract context grounding and semantic references."""
        # Simulated read-only extraction
        return {
            "source_type": "context",
            "raw_data": getattr(protocol_object, "model_dump", lambda: {})(),
        }


ParserRegistry.register("context", ContextParser)
