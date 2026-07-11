"""Evidence extractor for Conversation Generator."""

from aiodoo_datasets.generators.conversation.analysis.context import AnalysisContext
from aiodoo_datasets.generators.conversation.analysis.result import AnalysisResult
from aiodoo_datasets.generators.conversation.registries.parser_registry import ParserRegistry
import aiodoo_datasets.generators.conversation.analysis.parsers

class EvidenceExtractor:
    """Extracts immutable evidence and references from input protocols."""
    
    @staticmethod
    def extract(context: AnalysisContext) -> AnalysisResult:
        """Process all input protocols through their registered parsers."""
        evidence_pool = []
        
        for protocol_key, data in context.input_protocols.items():
            parser_cls = ParserRegistry.get_parser(protocol_key)
            if parser_cls:
                parser = parser_cls()
                extracted = parser.parse(data)
                evidence_pool.append(extracted)
                
        return AnalysisResult(evidence_pool=tuple(evidence_pool))
