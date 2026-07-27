#!/usr/bin/env python3
"""Step 6 — Regenerate Approval / Conversation / Evaluation production datasets.

Uses existing upstream JSONL (planner/coding/repair/execution/context).
Does not rebuild Development-adapter datasets or redesign generators.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import sys
import time
from pathlib import Path
from types import MappingProxyType
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("regenerate_v2")


def _load_jsonl(path: Path) -> tuple[dict[str, Any], ...]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                raise RuntimeError(f"Non-object JSONL record in {path}:{line_number}")
            records.append(record)
    return tuple(records)


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _count_lines(path: Path) -> int:
    count = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--datasets-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "datasets",
    )
    parser.add_argument(
        "--verify-reproducibility",
        action="store_true",
        help="Run Approval twice and require identical bytes (expensive).",
    )
    args = parser.parse_args()
    output_dir: Path = args.datasets_dir
    if not output_dir.is_dir():
        raise SystemExit(f"Datasets directory not found: {output_dir}")

    logger.info("Loading upstream datasets from %s", output_dir)
    planner = _load_jsonl(output_dir / "planner_v1_0.jsonl")
    coding = _load_jsonl(output_dir / "coding_v1_0.jsonl")
    repair = _load_jsonl(output_dir / "repair_v1_0.jsonl")
    execution = _load_jsonl(output_dir / "execution_dataset.jsonl")
    context_path = output_dir / "context_v1_0.jsonl"
    context = _load_jsonl(context_path) if context_path.exists() else ()

    logger.info(
        "Upstream counts: planner=%d coding=%d repair=%d execution=%d context=%d",
        len(planner),
        len(coding),
        len(repair),
        len(execution),
        len(context),
    )

    # ------------------------------------------------------------------
    # 1. Approval v2
    # ------------------------------------------------------------------
    from generators.approval.cli.configuration import build_pipeline_context
    from generators.approval.pipeline import ApprovalPipeline
    from generators.approval.version import SCHEMA_VERSION as APPROVAL_SCHEMA
    from generators.approval.version import __version__ as APPROVAL_VERSION

    logger.info("Starting Approval Generator v%s (schema %s)", APPROVAL_VERSION, APPROVAL_SCHEMA)
    t0 = time.perf_counter()
    approval_ns = argparse.Namespace(
        source_dir=Path("sources"),
        output_dir=output_dir,
        fail_fast=True,
        artifact_records={
            "planner": planner,
            "coding": coding,
            "repair": repair,
            "execution": execution,
        },
        protocol_context=None,
    )
    approval_result = ApprovalPipeline.generate(build_pipeline_context(approval_ns))
    if not approval_result.success:
        raise RuntimeError(f"Approval generation failed: {approval_result.diagnostics}")
    approval_path = output_dir / "approval_dataset.jsonl"
    approval_count = _count_lines(approval_path)
    logger.info(
        "Approval done: %d records in %.1fs checksum=%s",
        approval_count,
        time.perf_counter() - t0,
        _sha256(approval_path)[:16],
    )

    if args.verify_reproducibility:
        logger.info("Reproducibility check: regenerating Approval...")
        first = _sha256(approval_path)
        approval_result2 = ApprovalPipeline.generate(build_pipeline_context(approval_ns))
        if not approval_result2.success:
            raise RuntimeError(f"Approval regen failed: {approval_result2.diagnostics}")
        second = _sha256(approval_path)
        if first != second:
            raise RuntimeError("Approval reproducibility failed: checksum mismatch")
        logger.info("Approval reproducibility OK")

    approval_records = _load_jsonl(approval_path)

    # ------------------------------------------------------------------
    # 2. Conversation v2
    # ------------------------------------------------------------------
    from generators.conversation.cli.configuration import (
        build_pipeline_context as build_conversation_context,
    )
    from generators.conversation.pipeline import ConversationPipeline
    from generators.conversation.version import SCHEMA_VERSION as CONV_SCHEMA
    from generators.conversation.version import __version__ as CONV_VERSION

    logger.info("Starting Conversation Generator v%s (schema %s)", CONV_VERSION, CONV_SCHEMA)
    t0 = time.perf_counter()
    conversation_ns = argparse.Namespace(
        source_dir=Path("sources"),
        output_dir=output_dir,
        fail_fast=True,
        artifact_records={
            "planner": planner,
            "coding": coding,
            "repair": repair,
            "context": context,
            "execution": execution,
            "approval": approval_records,
        },
        protocol_context=None,
    )
    conversation_result = ConversationPipeline.generate(build_conversation_context(conversation_ns))
    if not conversation_result.success:
        raise RuntimeError(f"Conversation generation failed: {conversation_result.diagnostics}")
    conversation_path = output_dir / "conversation_dataset.jsonl"
    conversation_count = _count_lines(conversation_path)
    logger.info(
        "Conversation done: %d records in %.1fs checksum=%s",
        conversation_count,
        time.perf_counter() - t0,
        _sha256(conversation_path)[:16],
    )
    conversation_records = _load_jsonl(conversation_path)

    # ------------------------------------------------------------------
    # 3. Evaluation v2 (+ BenchmarkCatalog)
    # ------------------------------------------------------------------
    from generators.evaluation.cli.commands import Commands as EvalCommands
    from generators.evaluation.version import SCHEMA_VERSION as EVAL_SCHEMA
    from generators.evaluation.version import __version__ as EVAL_VERSION

    logger.info("Starting Evaluation Generator v%s (schema %s)", EVAL_VERSION, EVAL_SCHEMA)
    t0 = time.perf_counter()
    eval_config = {
        "source_protocols": MappingProxyType(
            {
                "planner": planner,
                "coding": coding,
                "repair": repair,
                "execution": execution,
                "context": context,
                "approval": approval_records,
                "conversation": conversation_records,
            }
        ),
        "evaluation_type": "standard",
        "target_generator": "aiodoo",
        "benchmark_name": "aiodoo_downstream_integration",
        "benchmark_category": "integration",
        "benchmark_description": "Evaluation judgments from AIODOO capability datasets.",
        "supported_odoo_versions": ["17.0", "18.0", "19.0"],
        "supported_protocols": (
            "planner",
            "coding",
            "repair",
            "execution",
            "context",
            "approval",
            "conversation",
        ),
        "generator_version": EVAL_VERSION,
        "protocol_version": "1.0",
        "schema_version": EVAL_SCHEMA,
    }
    eval_result = EvalCommands.run_generate(eval_config, str(output_dir))
    if not eval_result.validation_passed:
        raise RuntimeError("Evaluation generation reported validation_passed=False")
    evaluation_path = output_dir / "evaluation_dataset.jsonl"
    catalog_path = output_dir / "evaluation_benchmark_catalog.jsonl"
    evaluation_count = _count_lines(evaluation_path)
    catalog_count = _count_lines(catalog_path)
    logger.info(
        "Evaluation done: %d SFT + %d catalog in %.1fs",
        evaluation_count,
        catalog_count,
        time.perf_counter() - t0,
    )

    # ------------------------------------------------------------------
    # Summary JSON for the Step 6 report
    # ------------------------------------------------------------------
    summary = {
        "approval": {
            "path": str(approval_path),
            "records": approval_count,
            "generator_version": APPROVAL_VERSION,
            "schema_version": APPROVAL_SCHEMA,
            "checksum_sha256": _sha256(approval_path),
        },
        "conversation": {
            "path": str(conversation_path),
            "records": conversation_count,
            "generator_version": CONV_VERSION,
            "schema_version": CONV_SCHEMA,
            "checksum_sha256": _sha256(conversation_path),
        },
        "evaluation": {
            "path": str(evaluation_path),
            "records": evaluation_count,
            "generator_version": EVAL_VERSION,
            "schema_version": EVAL_SCHEMA,
            "checksum_sha256": _sha256(evaluation_path),
        },
        "evaluation_benchmark_catalog": {
            "path": str(catalog_path),
            "records": catalog_count,
            "checksum_sha256": _sha256(catalog_path),
            "training_forbidden": True,
        },
    }
    summary_path = output_dir / "step6_regeneration_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    logger.info("Wrote %s", summary_path)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
