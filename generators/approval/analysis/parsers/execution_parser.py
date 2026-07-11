"""Execution parser for the Approval Generator."""

from typing import Dict, Any, List
from aiodoo_datasets.generators.approval.domain.evidence import Evidence
from aiodoo_datasets.generators.approval.domain.source_generator import SourceGenerator
from aiodoo_datasets.generators.approval.analysis.parsers.base_parser import BaseParser
from aiodoo_datasets.generators.approval.analysis.parsers.parser_registry import ParserRegistry


@ParserRegistry.register("execution_data")
class ExecutionParser(BaseParser):
    """Parses Execution protocol data to extract evidence."""

    def parse(self, data: Dict[str, Any]) -> List[Evidence]:
        evidence_list = []
        if not data:
            return evidence_list

        # Example: extract test results
        tests = data.get("test_results", [])
        import hashlib

        for result in tests:
            source_ref = result.get("id", "unknown_test")
            hash_input = f"EXECUTION:{source_ref}"
            evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

            evidence_list.append(
                Evidence(
                    evidence_id=f"EVID-{evid_hash}",
                    source_generator=SourceGenerator.EXECUTION,
                    source_reference=source_ref,
                    file_path=result.get("file_path"),
                    snippet=result.get("error_message", "")[:200],
                    description=f"Test result: {result.get('name', '')} - {result.get('status', 'unknown')}",
                )
            )
        return evidence_list
