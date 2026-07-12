"""Planner Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class PlannerParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Planner protocol objects."""

    source_type = "planner"

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract planner instructions and structure."""
        return self._aggregate_records(protocol_object)


# Statically register parser
ParserRegistry.register("planner", PlannerParser)
