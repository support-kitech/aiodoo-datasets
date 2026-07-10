"""Coding parser for the Approval Generator."""

from typing import Dict, Any, List
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
from aiodoo_datasets.generators.approval.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.approval.analysis.parsers.parser_registry import ParserRegistry
@ParserRegistry.register("coding_data")
class CodingParser(BaseParser):
    """Parses Coding protocol data to extract evidence."""

    def parse(self, data: Dict[str, Any]) -> List[Evidence]:
        evidence_list = []
        if not data:
            return evidence_list
            
        # Example: extract source files generated
        files = data.get("files", [])
        import hashlib
        
        for file in files:
            source_ref = file.get("id", "unknown_file")
            hash_input = f"CODING:{source_ref}"
            evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
            
            evidence_list.append(
                Evidence(
                    evidence_id=f"EVID-{evid_hash}",
                    source_generator=SourceGenerator.CODING,
                    source_reference=source_ref,
                    file_path=file.get("path"),
                    snippet=file.get("content", "")[:200], # Keep a snippet
                    description=f"Generated code file: {file.get('path', '')}"
                )
            )
        return evidence_list
