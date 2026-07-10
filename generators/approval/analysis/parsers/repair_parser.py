"""Repair parser for the Approval Generator."""

from typing import Dict, Any, List
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
from aiodoo_datasets.generators.approval.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.approval.analysis.parsers.parser_registry import ParserRegistry
@ParserRegistry.register("repair_data")
class RepairParser(BaseParser):
    """Parses Repair protocol data to extract evidence."""

    def parse(self, data: Dict[str, Any]) -> List[Evidence]:
        evidence_list = []
        if not data:
            return evidence_list
            
        # Example: extract fixes applied
        fixes = data.get("fixes", [])
        import hashlib
        
        for fix in fixes:
            source_ref = fix.get("id", "unknown_fix")
            hash_input = f"REPAIR:{source_ref}"
            evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
            
            evidence_list.append(
                Evidence(
                    evidence_id=f"EVID-{evid_hash}",
                    source_generator=SourceGenerator.REPAIR,
                    source_reference=source_ref,
                    file_path=fix.get("file_path"),
                    snippet=fix.get("diff", "")[:200],
                    description=f"Applied fix: {fix.get('description', '')}"
                )
            )
        return evidence_list
