"""Repair parser for the Approval Generator."""

from typing import Any, List
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.source_generator import SourceGenerator
from generators.approval.analysis.parsers.base_parser import BaseParser
from generators.approval.analysis.parsers.parser_registry import ParserRegistry


@ParserRegistry.register("repair_data")
class RepairParser(BaseParser):  # type: ignore[misc]
    """Parses Repair protocol data to extract evidence."""

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
            tasks = output.get("tasks", []) if isinstance(output, dict) else []
            if not tasks:
                tasks = record.get("fixes", [])
            record_ref = record.get("metadata", {}).get("protocol_hash", "repair")

            for task in tasks:
                if not isinstance(task, dict):
                    continue
                source_ref = f"{record_ref}:{task.get('id', 'unknown_fix')}"
                hash_input = f"REPAIR:{source_ref}"
                evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
                artifacts = task.get("artifacts", [])
                first_artifact = (
                    artifacts[0] if artifacts and isinstance(artifacts[0], dict) else {}
                )
                expected_outcome = task.get("expected_outcome", {})

                evidence_list.append(
                    Evidence(
                        evidence_id=f"EVID-{evid_hash}",
                        source_generator=SourceGenerator.REPAIR,
                        source_reference=source_ref,
                        file_path=first_artifact.get("path"),
                        snippet=str(expected_outcome)[:200],
                        description=(
                            "Repair task: "
                            f"{task.get('description') or task.get('problem', {}).get('description', '')}"
                        ),
                    )
                )
        return evidence_list
