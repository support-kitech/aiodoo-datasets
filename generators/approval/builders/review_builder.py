"""Build one Approval Review (training unit) per subject."""

from __future__ import annotations

from typing import Any

from generators.approval.analysis import evidence_collector as _evidence_collector  # noqa: F401
from generators.approval.analysis.evidence_bounder import (
    bound_evidence,
    bound_findings,
    bound_recommendations,
)
from generators.approval.analysis.parsers.parser_registry import ParserRegistry
from generators.approval.analysis.subject import ApprovalSubject
from generators.approval.domain.decision import Decision
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.domain.review import Review
from generators.approval.engine.decision_engine import DecisionEngine
from generators.approval.engine.engine_context import EngineContext
from generators.approval.policy import MAX_REASONING_CHARS
from generators.approval.rules.rule_set import RuleSet


class SubjectReviewBuilder:
    """Run rules on subject-scoped evidence and emit one bounded Review."""

    @staticmethod
    def build(
        subject: ApprovalSubject,
        *,
        base_metadata: ReviewMetadata,
        rule_set: RuleSet,
        parser_registry_cls: type[ParserRegistry] = ParserRegistry,
    ) -> Review:
        parser = parser_registry_cls.get_parser(subject.data_key)
        if parser is None:
            evidence_full: tuple[Any, ...] = ()
        else:
            evidence_full = tuple(parser.parse(subject.source_record))

        metadata = ReviewMetadata(
            generator_version=base_metadata.generator_version,
            protocol_version=base_metadata.protocol_version,
            schema_version=base_metadata.schema_version,
            source_module=subject.module,
            odoo_version=base_metadata.odoo_version,
            odoo_edition=base_metadata.odoo_edition,
            planner_version=base_metadata.planner_version,
            coding_version=base_metadata.coding_version,
            execution_version=base_metadata.execution_version,
            repair_version=base_metadata.repair_version,
            complexity_score=base_metadata.complexity_score,
        )

        engine_result = DecisionEngine.execute(
            EngineContext(metadata=metadata, evidence_pool=evidence_full),
            rule_set,
        )

        decision = engine_result.decision
        reasoning = decision.reasoning
        if len(reasoning) > MAX_REASONING_CHARS:
            decision = Decision(
                decision_id=decision.decision_id,
                status=decision.status,
                confidence=decision.confidence,
                reasoning=reasoning[:MAX_REASONING_CHARS],
            )

        evidence = bound_evidence(evidence_full)
        findings = bound_findings(engine_result.findings)
        recommendations = bound_recommendations(engine_result.recommendations)
        finding_ids = {f.finding_id for f in findings}
        recommendations = tuple(r for r in recommendations if r.finding_id in finding_ids)

        payload = _build_payload(subject, evidence, findings, decision)

        return Review(
            review_id=subject.record_id,
            metadata=metadata,
            decision=decision,
            findings=findings,
            recommendations=recommendations,
            evidence=evidence,
            record_id=subject.record_id,
            capability=subject.capability,
            subject_id=subject.subject_id,
            source_object_id=subject.source_object_id,
            subject=subject.subject_label,
            payload=payload,
        )


def _build_payload(
    subject: ApprovalSubject,
    evidence: tuple[Any, ...],
    findings: tuple[Any, ...],
    decision: Decision,
) -> dict[str, Any]:
    evidence_summaries = [
        {
            "evidence_id": e.evidence_id,
            "source_generator": e.source_generator.value
            if hasattr(e.source_generator, "value")
            else str(e.source_generator),
            "source_reference": e.source_reference,
            "description": e.description,
        }
        for e in evidence
    ]
    finding_summaries = [
        {
            "finding_id": f.finding_id,
            "rule_id": f.rule_id,
            "severity": f.severity.value if hasattr(f.severity, "value") else str(f.severity),
            "description": f.description,
        }
        for f in findings
    ]
    return {
        "record_id": subject.record_id,
        "capability": subject.capability,
        "subject_id": subject.subject_id,
        "source_object_id": subject.source_object_id,
        "module": subject.module,
        "decision_status": decision.status.value,
        "evidence_count": len(evidence),
        "evidence": evidence_summaries,
        "findings": finding_summaries,
    }
