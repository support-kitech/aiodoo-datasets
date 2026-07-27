"""Bound evidence / findings written into Approval training records."""

from __future__ import annotations

from typing import Sequence

from generators.approval.domain.evidence import Evidence
from generators.approval.domain.finding import Finding
from generators.approval.domain.recommendation import Recommendation
from generators.approval.policy import (
    MAX_DESCRIPTION_CHARS,
    MAX_EVIDENCE_ITEMS,
    MAX_FINDINGS,
    MAX_RECOMMENDATIONS,
    MAX_SNIPPET_CHARS,
)


def bound_evidence(
    evidence: Sequence[Evidence],
    *,
    limit: int = MAX_EVIDENCE_ITEMS,
) -> tuple[Evidence, ...]:
    """Return a deterministic, size-capped evidence tuple for dataset export."""
    ordered = sorted(evidence, key=lambda e: e.evidence_id)
    capped: list[Evidence] = []
    for item in ordered[: max(0, limit)]:
        snippet = item.snippet
        if isinstance(snippet, str) and len(snippet) > MAX_SNIPPET_CHARS:
            snippet = snippet[:MAX_SNIPPET_CHARS]
        description = item.description or ""
        if len(description) > MAX_DESCRIPTION_CHARS:
            description = description[:MAX_DESCRIPTION_CHARS]
        capped.append(
            Evidence(
                evidence_id=item.evidence_id,
                source_generator=item.source_generator,
                source_reference=item.source_reference,
                file_path=item.file_path,
                line_number=item.line_number,
                snippet=snippet,
                description=description,
            )
        )
    return tuple(capped)


def bound_findings(
    findings: Sequence[Finding],
    *,
    limit: int = MAX_FINDINGS,
) -> tuple[Finding, ...]:
    ordered = sorted(findings, key=lambda f: f.finding_id)
    result: list[Finding] = []
    for finding in ordered[: max(0, limit)]:
        evidence = bound_evidence(finding.evidence, limit=min(8, MAX_EVIDENCE_ITEMS))
        description = finding.description
        if len(description) > MAX_DESCRIPTION_CHARS:
            description = description[:MAX_DESCRIPTION_CHARS]
        result.append(
            Finding(
                finding_id=finding.finding_id,
                rule_id=finding.rule_id,
                category=finding.category,
                severity=finding.severity,
                description=description,
                evidence=evidence,
                is_positive=finding.is_positive,
            )
        )
    return tuple(result)


def bound_recommendations(
    recommendations: Sequence[Recommendation],
    *,
    limit: int = MAX_RECOMMENDATIONS,
) -> tuple[Recommendation, ...]:
    ordered = sorted(recommendations, key=lambda r: r.recommendation_id)
    return tuple(ordered[: max(0, limit)])
