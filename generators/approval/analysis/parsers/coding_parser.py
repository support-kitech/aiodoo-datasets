"""Coding parser for the Approval Generator."""

from typing import Any, List
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.source_generator import SourceGenerator
from generators.approval.analysis.parsers.base_parser import BaseParser
from generators.approval.analysis.parsers.parser_registry import ParserRegistry


@ParserRegistry.register("coding_data")
class CodingParser(BaseParser):  # type: ignore[misc]
    """Parses Coding protocol data to extract evidence."""

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
            artifacts = output.get("artifacts", []) if isinstance(output, dict) else []
            legacy_artifacts = False
            if not artifacts:
                artifacts = record.get("files", [])
                legacy_artifacts = True
            record_ref = record.get("metadata", {}).get("protocol_hash", "coding")

            for artifact in artifacts:
                if not isinstance(artifact, dict):
                    continue
                artifact_id = artifact.get("id", "unknown_file")
                source_ref = artifact_id if legacy_artifacts else f"{record_ref}:{artifact_id}"
                hash_input = f"CODING:{source_ref}"
                evid_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
                snippet = (
                    artifact.get("diff") or artifact.get("intent") or artifact.get("reason", "")
                )

                evidence_list.append(
                    Evidence(
                        evidence_id=f"EVID-{evid_hash}",
                        source_generator=SourceGenerator.CODING,
                        source_reference=source_ref,
                        file_path=artifact.get("path"),
                        snippet=str(snippet)[:200],
                        description=f"Generated code artifact: {artifact.get('path', '')}",
                    )
                )
        return evidence_list
