"""Context Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class ContextParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Context protocol objects."""

    source_type = "context"

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract context grounding and semantic references."""
        return self._aggregate_records(protocol_object)


ParserRegistry.register("context", ContextParser)
