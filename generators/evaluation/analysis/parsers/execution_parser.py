"""Execution Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class ExecutionParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Execution protocol objects."""

    source_type = "execution"

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract execution output and environment context."""
        return self._aggregate_records(protocol_object)


ParserRegistry.register("execution", ExecutionParser)
