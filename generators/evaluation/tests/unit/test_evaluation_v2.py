"""Unit tests for Evaluation v2 judgment grain and catalog separation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from generators.common.contract.adapters import project_evaluation
from generators.evaluation.builders.judgment_builder import JudgmentBuilder
from generators.evaluation.identity import compute_candidate_id, compute_record_id
from generators.evaluation.pipeline.pipeline import EvaluationPipeline
from generators.evaluation.pipeline.pipeline_context import PipelineContext
from generators.evaluation import api


def _row(capability: str, module: str, protocol_hash: str) -> dict:
    if capability == "planner":
        output = {"goal": "plan", "tasks": [{"id": "t1", "description": "step"}]}
    elif capability == "coding":
        output = {"goal": "code", "artifacts": [{"id": "a1", "path": "a.py"}]}
    elif capability == "repair":
        output = {"goal": "fix", "tasks": [{"id": "r1", "description": "fix"}]}
    else:
        output = {"execution_id": f"ex-{protocol_hash}", "steps": [{"id": "s1"}], "summary": "ok"}
    return {
        "instruction": f"{capability} work",
        "output": output,
        "metadata": {"module": module, "protocol_hash": protocol_hash},
    }


class TestEvaluationIdentity(unittest.TestCase):
    def test_ids_deterministic(self) -> None:
        c1 = compute_candidate_id("coding", "hash1")
        c2 = compute_candidate_id("coding", "hash1")
        self.assertEqual(c1, c2)
        self.assertTrue(c1.startswith("CAND-"))
        r1 = compute_record_id(c1, "pass")
        self.assertEqual(r1, compute_record_id(c1, "pass"))
        self.assertNotEqual(r1, compute_record_id(c1, "fail"))
        self.assertTrue(r1.startswith("EVL-"))


class TestJudgmentBuilder(unittest.TestCase):
    def test_emits_pass_fail_inconclusive_per_candidate(self) -> None:
        protocols = {
            "planner": (_row("planner", "sale", "p1"),),
            "coding": (_row("coding", "sale", "c1"),),
            "repair": (_row("repair", "sale", "r1"),),
            "execution": (_row("execution", "sale", "e1"),),
        }
        cases = JudgmentBuilder.build_all(protocols)
        self.assertEqual(len(cases), 4 * 3)
        keys = {(c.candidate_id, c.evaluation_case_key) for c in cases}
        self.assertEqual(len(keys), len(cases))
        verdicts = {c.verdict for c in cases}
        self.assertEqual(verdicts, {"pass", "fail", "inconclusive"})
        self.assertEqual([c.record_id for c in cases], sorted(c.record_id for c in cases))


class TestEvaluationPipeline(unittest.TestCase):
    def test_sft_and_catalog_are_separate(self) -> None:
        protocols = {
            "planner": (_row("planner", "m", "p1"),),
            "coding": (_row("coding", "m", "c1"),),
            "repair": (_row("repair", "m", "r1"),),
            "execution": (_row("execution", "m", "e1"),),
        }
        context = PipelineContext(
            source_protocols=protocols,
            evaluation_type="standard",
            target_generator="aiodoo",
            benchmark_name="test_bench",
            benchmark_category="unit",
            benchmark_description="test",
            supported_odoo_versions=("18.0",),
            supported_protocols=tuple(protocols.keys()),
            generator_version="2.0.0",
            protocol_version="1.0",
            schema_version="2.0",
        )
        result = EvaluationPipeline.run(context)
        self.assertTrue(result.validation_passed)
        self.assertGreaterEqual(len(result.dataset), 2)
        self.assertIsInstance(result.dataset[0], dict)
        self.assertIn("verdict", result.dataset[0])
        self.assertNotIn("catalog", result.dataset[0])
        self.assertIsNotNone(result.catalog)
        assert result.catalog is not None
        self.assertIn("catalog", result.catalog)
        self.assertTrue(result.catalog["metadata"]["training_forbidden"])

        for record in result.dataset:
            projection = project_evaluation(record)
            self.assertEqual(projection.capability, "evaluation")

        with tempfile.TemporaryDirectory() as tmp:
            exported = EvaluationPipeline.export(result, tmp)
            self.assertTrue(exported.validation_passed)
            sft = Path(tmp) / "evaluation_dataset.jsonl"
            catalog = Path(tmp) / "evaluation_benchmark_catalog.jsonl"
            self.assertTrue(sft.exists())
            self.assertTrue(catalog.exists())
            sft_lines = [ln for ln in sft.read_text().splitlines() if ln.strip()]
            cat_lines = [ln for ln in catalog.read_text().splitlines() if ln.strip()]
            self.assertGreaterEqual(len(sft_lines), 2)
            self.assertEqual(len(cat_lines), 1)
            self.assertNotIn("catalog", json.loads(sft_lines[0]))
            self.assertIn("catalog", json.loads(cat_lines[0]))

            # Reproducibility
            result2 = EvaluationPipeline.run(context)
            EvaluationPipeline.export(result2, tmp)
            self.assertEqual(
                sft.read_bytes(), (Path(tmp) / "evaluation_dataset.jsonl").read_bytes()
            )

    def test_api_validate_accepts_judgments(self) -> None:
        protocols = {
            "planner": (_row("planner", "m", "p1"),),
            "coding": (_row("coding", "m", "c1"),),
            "repair": (_row("repair", "m", "r1"),),
            "execution": (_row("execution", "m", "e1"),),
        }
        result = api.generate(
            {
                "source_protocols": protocols,
                "benchmark_name": "api_bench",
                "benchmark_category": "unit",
            }
        )
        self.assertTrue(api.validate(result.dataset))


if __name__ == "__main__":
    unittest.main()
