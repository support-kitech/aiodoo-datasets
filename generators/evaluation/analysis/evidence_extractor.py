"""Evidence Extractor for Evaluation Generator."""

from typing import Tuple, Any
from types import MappingProxyType
from generators.evaluation.analysis.context import AnalysisContext
from generators.evaluation.registries.parser_registry import ParserRegistry


class EvidenceExtractor:
    """Orchestrates parsers to extract evaluation evidence deterministically."""

    @staticmethod
    def extract(context: AnalysisContext) -> Tuple[MappingProxyType[str, Any], ...]:
        """Route protocols to the correct parsers and aggregate evidence."""
        evidence = []
        for source_type, protocol_obj in context.source_protocols.items():
            parser_class = ParserRegistry.get(source_type)
            if parser_class:
                parser_instance = parser_class()
                # Parse without mutating
                extracted = parser_instance.parse(protocol_obj)
                evidence.append(MappingProxyType(extracted))

        # Sort or structure evidence deterministically
        evidence.sort(key=lambda x: x.get("source_type", ""))
        return tuple(evidence)
