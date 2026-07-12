"""Execution parser for the Approval Generator."""

from typing import Any, List
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.source_generator import SourceGenerator
from generators.approval.analysis.parsers.base_parser import BaseParser
from generators.approval.analysis.parsers.parser_registry import ParserRegistry


@ParserRegistry.register("execution_data")
class ExecutionParser(BaseParser):  # type: ignore[misc]
    """Parses Execution protocol data to extract evidence."""

    def parse(self, data: Any) -> List[Evidence]:
        evidence_list = []  # type: ignore[var-annotated]
        if not data:
            return evidence_list

        import hashlib

        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            output = record.get("output", {})
            steps = output.get("steps", []) if isinstance(output, dict) else []
            if not steps:
                steps = record.get("test_results", [])
            execution_id = (
                output.get("execution_id", "execution") if isinstance(output, dict) else "execution"
            )

            for step in steps:
                if not isinstance(step, dict):
                    continue
                source_ref = f"{execution_id}:{step.get('id', 'unknown_step')}"
                hash_input = f"EXECUTION:{source_ref}"
                evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]

                evidence_list.append(
                    Evidence(
                        evidence_id=f"EVID-{evid_hash}",
                        source_generator=SourceGenerator.EXECUTION,
                        source_reference=source_ref,
                        file_path=step.get("path"),
                        snippet=str(step)[:200],
                        description=(
                            f"Execution step: {step.get('action') or step.get('name', '')}"
                        ),
                    )
                )
        return evidence_list
