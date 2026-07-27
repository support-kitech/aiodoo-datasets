"""Build Evaluation capability SFT judgments from upstream capability rows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from generators.evaluation.identity import compute_candidate_id, compute_record_id
from generators.evaluation.policy import (
    FAIL_CASE_KEY,
    INCONCLUSIVE_CASE_KEY,
    MAX_RECORDS_PER_CAPABILITY,
    OPTIONAL_SOURCE_TYPES,
    PASS_CASE_KEY,
    REQUIRED_SOURCE_TYPES,
)
from generators.evaluation.version import SCHEMA_VERSION, __version__


@dataclass(frozen=True, slots=True)
class JudgmentCase:
    """One EvaluationRequest/Response training unit (pre-serialization)."""

    record_id: str
    candidate_id: str
    evaluation_case_key: str
    capability_under_test: str
    candidate: dict[str, Any]
    expectation: dict[str, Any] | None
    rubric: str
    verdict: str
    score: float | None
    explanation: str
    module: str


class JudgmentBuilder:
    """Extract deterministic pass/fail/inconclusive judgments from upstream JSONL."""

    @staticmethod
    def build_all(source_protocols: Mapping[str, Any]) -> tuple[JudgmentCase, ...]:
        cases: list[JudgmentCase] = []
        seen: set[str] = set()

        for capability in (*REQUIRED_SOURCE_TYPES, *OPTIONAL_SOURCE_TYPES):
            rows = _as_records(source_protocols.get(capability))
            if not rows:
                continue
            limit = MAX_RECORDS_PER_CAPABILITY.get(capability)
            ordered = sorted(rows, key=lambda r: _source_object_id(capability, r))
            if limit is not None:
                ordered = ordered[:limit]

            for record in ordered:
                source_object_id = _source_object_id(capability, record)
                candidate_id = compute_candidate_id(capability, source_object_id)
                module = _module_name(record)
                gold = _candidate_payload(capability, record)

                for case in _cases_for_candidate(
                    capability=capability,
                    candidate_id=candidate_id,
                    module=module,
                    gold=gold,
                ):
                    if case.record_id in seen:
                        continue
                    seen.add(case.record_id)
                    cases.append(case)

        cases.sort(key=lambda c: c.record_id)
        return tuple(cases)


def judgment_to_record(case: JudgmentCase) -> dict[str, Any]:
    """Serialize a JudgmentCase to a contract-projectable JSONL record."""
    return {
        "record_id": case.record_id,
        "candidate_id": case.candidate_id,
        "evaluation_case_key": case.evaluation_case_key,
        "capability_under_test": case.capability_under_test,
        "candidate": case.candidate,
        "expectation": case.expectation,
        "rubric": case.rubric,
        "verdict": case.verdict,
        "score": case.score,
        "explanation": case.explanation,
        "metadata": {
            "module": case.module,
            "protocol_version": "1.0",
            "schema_version": SCHEMA_VERSION,
            "generator_version": __version__,
            "capability_under_test": case.capability_under_test,
            "candidate_id": case.candidate_id,
            "evaluation_case_key": case.evaluation_case_key,
            "record_id": case.record_id,
        },
    }


def _cases_for_candidate(
    *,
    capability: str,
    candidate_id: str,
    module: str,
    gold: dict[str, Any],
) -> tuple[JudgmentCase, ...]:
    rubric = (
        f"Judge whether the {capability} candidate satisfies the expectation "
        "for an Odoo development artifact."
    )
    pass_key = PASS_CASE_KEY
    fail_key = FAIL_CASE_KEY
    incon_key = INCONCLUSIVE_CASE_KEY

    pass_case = JudgmentCase(
        record_id=compute_record_id(candidate_id, pass_key),
        candidate_id=candidate_id,
        evaluation_case_key=pass_key,
        capability_under_test=capability,
        candidate=dict(gold),
        expectation=dict(gold),
        rubric=rubric,
        verdict="pass",
        score=1.0,
        explanation=f"Candidate matches the expected {capability} artifact.",
        module=module,
    )
    fail_candidate = {
        "capability": capability,
        "status": "invalid",
        "output": {},
        "error": "deliberately broken candidate for fail-case training",
    }
    fail_case = JudgmentCase(
        record_id=compute_record_id(candidate_id, fail_key),
        candidate_id=candidate_id,
        evaluation_case_key=fail_key,
        capability_under_test=capability,
        candidate=fail_candidate,
        expectation=dict(gold),
        rubric=rubric,
        verdict="fail",
        score=0.0,
        explanation=f"Candidate is missing required {capability} structure.",
        module=module,
    )
    incon_case = JudgmentCase(
        record_id=compute_record_id(candidate_id, incon_key),
        candidate_id=candidate_id,
        evaluation_case_key=incon_key,
        capability_under_test=capability,
        candidate=dict(gold),
        expectation=None,
        rubric=rubric,
        verdict="inconclusive",
        score=None,
        explanation="Expectation is unavailable; verdict cannot be decided confidently.",
        module=module,
    )
    return (pass_case, fail_case, incon_case)


def _as_records(raw: Any) -> tuple[Mapping[str, Any], ...]:
    if raw is None:
        return ()
    if isinstance(raw, Mapping):
        if any(k in raw for k in ("metadata", "output", "instruction", "query", "decision")):
            return (raw,)
        return ()
    if isinstance(raw, (list, tuple)):
        return tuple(r for r in raw if isinstance(r, Mapping))
    return ()


def _module_name(record: Mapping[str, Any]) -> str:
    meta = record.get("metadata")
    if isinstance(meta, Mapping):
        module = meta.get("module") or meta.get("source_module")
        if isinstance(module, str) and module.strip():
            return module.strip()
    return "unknown"


def _source_object_id(capability: str, record: Mapping[str, Any]) -> str:
    if isinstance(record.get("record_id"), str) and record["record_id"].strip():
        return str(record["record_id"]).strip()
    meta = record.get("metadata") if isinstance(record.get("metadata"), Mapping) else {}
    ph = meta.get("protocol_hash")
    if isinstance(ph, str) and ph.strip():
        return ph.strip()
    output = record.get("output") if isinstance(record.get("output"), Mapping) else {}
    if capability == "execution":
        eid = output.get("execution_id")
        if isinstance(eid, str) and eid.strip():
            return eid.strip()
    if capability == "context":
        cid = record.get("id")
        if isinstance(cid, str) and cid.strip():
            return cid.strip()
    instruction = record.get("instruction") or record.get("query") or ""
    return f"{capability}:{_module_name(record)}:{str(instruction)[:64]}"


def _candidate_payload(capability: str, record: Mapping[str, Any]) -> dict[str, Any]:
    """Bounded candidate dump for EvaluationRequest.candidate."""
    payload: dict[str, Any] = {"capability": capability}
    if "instruction" in record:
        payload["instruction"] = str(record.get("instruction", ""))[:500]
    if "query" in record:
        payload["query"] = str(record.get("query", ""))[:500]
    output = record.get("output")
    if isinstance(output, Mapping):
        # Keep a compact view — never dump megabyte artifacts wholesale.
        compact: dict[str, Any] = {}
        for key in ("goal", "summary", "execution_id", "module"):
            if key in output:
                compact[key] = output[key]
        for list_key in ("tasks", "artifacts", "steps"):
            value = output.get(list_key)
            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                compact[list_key] = list(value)[:8]
        payload["output"] = compact
    decision = record.get("decision")
    if isinstance(decision, Mapping):
        payload["decision"] = {
            "status": decision.get("status"),
            "reasoning": str(decision.get("reasoning", ""))[:400],
        }
    if "subject" in record:
        payload["subject"] = str(record.get("subject", ""))[:300]
    meta = record.get("metadata")
    if isinstance(meta, Mapping):
        payload["metadata"] = {
            "module": meta.get("module") or meta.get("source_module"),
            "protocol_hash": meta.get("protocol_hash"),
        }
    return payload
