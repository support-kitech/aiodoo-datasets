"""Unit tests for Approval subject partitioning, identity, bounds, and pipeline grain."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from generators.approval.analysis.evidence_bounder import bound_evidence
from generators.approval.analysis.subject import SubjectPartitioner
from generators.approval.config.approval_config import ApprovalConfig
from generators.approval.domain.evidence import Evidence
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.domain.source_generator import SourceGenerator
from generators.approval.identity import compute_record_id
from generators.approval.pipeline import ApprovalPipeline
from generators.approval.pipeline_context import PipelineContext
from generators.approval.policy import MAX_EVIDENCE_ITEMS
from generators.approval.rules.registry import RuleRegistry
from generators.common.contract.adapters import project_approval


def _upstream_record(
    *,
    capability: str,
    module: str,
    protocol_hash: str,
    instruction: str = "do work",
) -> dict:
    output: dict
    if capability == "planner":
        output = {"goal": instruction, "tasks": [{"id": "t1", "description": "plan"}]}
    elif capability == "coding":
        output = {
            "goal": instruction,
            "artifacts": [{"id": "a1", "path": "models.py", "intent": "add model"}],
        }
    elif capability == "repair":
        output = {
            "goal": instruction,
            "tasks": [{"id": "r1", "description": "fix bug", "artifacts": []}],
        }
    else:
        output = {
            "execution_id": f"exec-{protocol_hash}",
            "steps": [{"id": "s1", "action": "run", "path": "tests.py"}],
        }
    return {
        "instruction": instruction,
        "output": output,
        "metadata": {
            "module": module,
            "protocol_hash": protocol_hash,
            "protocol_version": "1.0",
            "schema_version": "1.0",
        },
    }


class TestApprovalIdentity(unittest.TestCase):
    def test_record_id_deterministic(self) -> None:
        a = compute_record_id("coding", "coding:sale:h1", "h1")
        b = compute_record_id("coding", "coding:sale:h1", "h1")
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("APR-"))
        self.assertEqual(len(a), 4 + 32)

    def test_record_id_changes_with_inputs(self) -> None:
        a = compute_record_id("coding", "coding:sale:h1", "h1")
        b = compute_record_id("repair", "repair:sale:h1", "h1")
        self.assertNotEqual(a, b)


class TestSubjectPartitioner(unittest.TestCase):
    def test_extracts_one_subject_per_upstream_row(self) -> None:
        protocols = {
            "planner_data": (
                _upstream_record(capability="planner", module="sale", protocol_hash="p1"),
                _upstream_record(capability="planner", module="sale", protocol_hash="p2"),
            ),
            "coding_data": (
                _upstream_record(capability="coding", module="sale", protocol_hash="c1"),
            ),
            "repair_data": (
                _upstream_record(capability="repair", module="sale", protocol_hash="r1"),
            ),
            "execution_data": (
                _upstream_record(capability="execution", module="sale", protocol_hash="e1"),
            ),
        }
        subjects = SubjectPartitioner.extract(protocols)
        self.assertEqual(len(subjects), 5)
        ids = [s.record_id for s in subjects]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(set(ids)), 5)
        caps = {s.capability for s in subjects}
        self.assertEqual(caps, {"planner", "coding", "repair", "execution"})

    def test_deduplicates_identical_subjects(self) -> None:
        row = _upstream_record(capability="coding", module="sale", protocol_hash="same")
        protocols = {
            "planner_data": (),
            "coding_data": (row, dict(row)),
            "repair_data": (),
            "execution_data": (),
        }
        subjects = SubjectPartitioner.extract(protocols)
        self.assertEqual(len(subjects), 1)


class TestEvidenceBounder(unittest.TestCase):
    def test_bounds_and_sorts(self) -> None:
        evidence = [
            Evidence(
                evidence_id=f"EVID-{i:04d}",
                source_generator=SourceGenerator.CODING,
                source_reference=f"ref-{i}",
                snippet="x" * 500,
                description="d" * 500,
            )
            for i in range(MAX_EVIDENCE_ITEMS + 10)
        ]
        bounded = bound_evidence(evidence)
        self.assertEqual(len(bounded), MAX_EVIDENCE_ITEMS)
        self.assertEqual([e.evidence_id for e in bounded], sorted(e.evidence_id for e in bounded))
        self.assertLessEqual(len(bounded[0].snippet or ""), 200)


class TestApprovalPipelineGrain(unittest.TestCase):
    def test_emits_one_record_per_subject_sorted(self) -> None:
        protocols = {
            "planner_data": (
                _upstream_record(capability="planner", module="m", protocol_hash="p1"),
            ),
            "coding_data": (_upstream_record(capability="coding", module="m", protocol_hash="c1"),),
            "repair_data": (_upstream_record(capability="repair", module="m", protocol_hash="r1"),),
            "execution_data": (
                _upstream_record(capability="execution", module="m", protocol_hash="e1"),
            ),
        }
        with tempfile.TemporaryDirectory() as tmp:
            context = PipelineContext(
                config=ApprovalConfig(
                    output_dir=tmp,
                    manifest_path=str(Path(tmp) / "dataset_manifest.json"),
                ),
                input_protocols=protocols,
                metadata=ReviewMetadata(
                    generator_version="2.0.0",
                    protocol_version="1.0",
                    schema_version="2.0",
                    source_module="m",
                ),
                rule_set=RuleRegistry.compile(),
            )
            result = ApprovalPipeline.generate(context)
            self.assertTrue(result.success, result.diagnostics)
            jsonl = Path(tmp) / "approval_dataset.jsonl"
            lines = [ln for ln in jsonl.read_text(encoding="utf-8").splitlines() if ln.strip()]
            self.assertEqual(len(lines), 4)
            records = [json.loads(ln) for ln in lines]
            record_ids = [r["record_id"] for r in records]
            self.assertEqual(record_ids, sorted(record_ids))
            self.assertEqual(len(set(record_ids)), 4)
            for rec in records:
                self.assertEqual(rec["review_id"], rec["record_id"])
                self.assertLessEqual(len(rec["evidence"]), MAX_EVIDENCE_ITEMS)
                self.assertEqual(rec["record_id"][:4], "APR-")
                projection = project_approval(rec)
                self.assertEqual(projection.capability, "approval")
                self.assertTrue(projection.request.subject)
                self.assertIn("subject_id", projection.request.payload)

            stats = json.loads((Path(tmp) / "approval_statistics.json").read_text())
            self.assertGreaterEqual(stats.get("total_samples", 0), 4)

            # Reproducibility: same inputs → identical JSONL bytes
            result2 = ApprovalPipeline.generate(context)
            self.assertTrue(result2.success)
            self.assertEqual(
                jsonl.read_bytes(),
                (Path(tmp) / "approval_dataset.jsonl").read_bytes(),
            )


class TestProjectApprovalSubjectPayload(unittest.TestCase):
    def test_prefers_explicit_subject_and_payload(self) -> None:
        record = {
            "review_id": "APR-" + ("b" * 32),
            "record_id": "APR-" + ("b" * 32),
            "subject": "Approve coding artifact xyz (sale)",
            "payload": {"subject_id": "coding:sale:xyz", "evidence_count": 2},
            "decision": {"status": "APPROVED", "reasoning": "ok"},
            "metadata": {"source_module": "sale"},
            "evidence": [{}, {}],
        }
        projection = project_approval(record)
        self.assertEqual(projection.request.subject, "Approve coding artifact xyz (sale)")
        self.assertEqual(projection.request.payload["subject_id"], "coding:sale:xyz")


if __name__ == "__main__":
    unittest.main()
