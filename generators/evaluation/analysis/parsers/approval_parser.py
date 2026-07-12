"""Approval Parser for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation.analysis.parsers.base_parser import BaseParser
from generators.evaluation.registries.parser_registry import ParserRegistry


class ApprovalParser(BaseParser):  # type: ignore[misc]
    """Extracts deterministic evidence from Approval protocol objects."""

    source_type = "approval"

    def parse(self, protocol_object: Any) -> Dict[str, Any]:
        """Extract review feedback and verification metadata."""
        return self._aggregate_records(protocol_object)


ParserRegistry.register("approval", ApprovalParser)
