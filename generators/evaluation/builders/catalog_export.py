"""Build a separate BenchmarkCatalog artifact (non-SFT) from judgment cases."""

from __future__ import annotations

from typing import Any, Sequence

from generators.evaluation.builders.judgment_builder import JudgmentCase
from generators.evaluation.policy import ID_SCHEME_VERSION
from generators.evaluation.version import SCHEMA_VERSION, __version__


def build_benchmark_catalog_record(
    cases: Sequence[JudgmentCase],
    *,
    benchmark_name: str,
    benchmark_category: str,
    benchmark_description: str,
    target_generator: str,
) -> dict[str, Any]:
    """Serialize one BenchmarkCatalog JSON object for certification / regression.

    This is intentionally a single aggregate artifact — not an SFT training unit.
    """
    by_capability: dict[str, list[dict[str, Any]]] = {}
    for case in cases:
        by_capability.setdefault(case.capability_under_test, []).append(
            {
                "case_id": case.record_id,
                "candidate_id": case.candidate_id,
                "evaluation_case_key": case.evaluation_case_key,
                "expected_verdict": case.verdict,
                "module": case.module,
                "difficulty": _difficulty_for_key(case.evaluation_case_key),
            }
        )

    suites = []
    for capability in sorted(by_capability.keys()):
        suite_cases = sorted(by_capability[capability], key=lambda c: c["case_id"])
        suites.append(
            {
                "suite_id": f"SUITE-{capability}",
                "suite_name": f"{capability} evaluation suite",
                "suite_category": benchmark_category,
                "cases": suite_cases,
            }
        )

    catalog_id = f"CTLG-{benchmark_name.replace(' ', '_')[:48]}"
    return {
        "evaluation_id": f"EVALROOT-{benchmark_name.replace(' ', '_')[:40]}",
        "catalog": {
            "catalog_id": catalog_id,
            "catalog_name": benchmark_name,
            "catalog_description": benchmark_description,
            "suites": suites,
        },
        "metadata": {
            "protocol_version": "1.0",
            "schema_version": SCHEMA_VERSION,
            "generator_version": __version__,
            "id_scheme_version": ID_SCHEME_VERSION,
            "benchmark_category": benchmark_category,
            "target_generator": target_generator,
            "case_count": len(cases),
            "suite_count": len(suites),
            "artifact_role": "benchmark_catalog",
            "training_forbidden": True,
        },
    }


def _difficulty_for_key(case_key: str) -> str:
    if case_key == "fail":
        return "hard"
    if case_key == "inconclusive":
        return "medium"
    return "easy"
