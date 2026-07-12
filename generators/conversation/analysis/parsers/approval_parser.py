"""Approval parser for Conversation Generator."""

from typing import Dict, Any
from types import MappingProxyType
from generators.conversation.analysis.parsers.base_parser import BaseParser
from generators.conversation.registries.parser_registry import ParserRegistry
from generators.conversation.analysis.result import ExtractedEvidence
from generators.conversation.domain.reference import Reference


@ParserRegistry.register("approval_protocol")
class ApprovalParser(BaseParser):  # type: ignore[misc]
    """Parses Approval protocols."""

    def parse(self, data: Dict[str, Any]) -> ExtractedEvidence:
        references = []
        records = data if isinstance(data, (list, tuple)) else (data,)
        for record in records:
            if not isinstance(record, dict):
                continue
            findings = record.get("findings", [])
            if findings:
                for finding in findings:
                    if not isinstance(finding, dict):
                        continue
                    references.append(
                        Reference(
                            source_generator="approval",
                            source_reference=finding.get("finding_id", "unknown"),
                            description=f"Approval finding: {finding.get('description', '')}",
                        )
                    )
                    if len(references) >= 25:
                        break
            else:
                decision = record.get("decision", {})
                references.append(
                    Reference(
                        source_generator="approval",
                        source_reference=record.get("review_id", "unknown"),
                        description=f"Approval decision: {decision.get('status', '')}",
                    )
                )
            if len(references) >= 25:
                break
        return ExtractedEvidence(
            protocol_name="approval_protocol",
            references=tuple(references),
            attachments=(),
            raw_data=MappingProxyType({"record_count": len(records)}),
        )
