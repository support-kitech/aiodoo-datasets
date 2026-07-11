"""Evidence Collector for the Approval Generator."""

from typing import List, Mapping, Any
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.analysis.parsers.parser_registry import ParserRegistry
from aiodoo_datasets.generators.approval.analysis.parsers import (
    coding_parser,
    execution_parser,
    planner_parser,
    repair_parser
)

__all__ = [
    "coding_parser",
    "execution_parser",
    "planner_parser",
    "repair_parser"
]

class EvidenceCollector:
    """Collects and aggregates evidence from upstream protocol data."""
    
    @staticmethod
    def collect(input_protocols: Mapping[str, Mapping[str, Any]]) -> List[Evidence]:
        """Iterate through the ParserRegistry and extract evidence from all inputs."""
        all_evidence = []
        
        parsers = ParserRegistry.get_all_parsers()
        
        for data_key, parser in parsers.items():
            protocol_data = input_protocols.get(data_key, {})
            if protocol_data:
                evidence = parser.parse(protocol_data)
                all_evidence.extend(evidence)
                
        return all_evidence
