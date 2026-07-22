"""Produce a per-capability evaluation corpus using canonical `aiodoo_contract` schemas.

This closes ACT-007 / DEF-05 (`ecosystem-v2-certification/MASTER_ACTION_LIST.md`,
`ARCHITECTURE_FREEZE_REPORT.md` Tier 1): today, `aiodoo-datasets` produces
training JSONL for every capability but has **no** eval corpus producer at
all, so `aiodoo-validation` has nothing durable to certify against.

Each eval corpus record is a `(request, expected_response)` gold pair built
with the *same* `aiodoo_contract` schema classes used everywhere else in the
ecosystem — not a bespoke evaluation-specific shape — so a consumer never
needs a second parser to read it. Records that cannot be projected onto the
contract (see :mod:`generators.common.contract.adapters`) are skipped and
counted, never silently dropped without a trace.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from aiodoo_contract.validators import ContractValidator

from generators.common.contract.adapters import (
    SUPPORTED_CAPABILITIES,
    ContractAdapterError,
    project_record,
)
from generators.common.statistics.base_statistics import BaseStatistics

__all__ = [
    "EvalCorpusBuildReport",
    "build_eval_corpus",
    "write_eval_corpus",
    "DEFAULT_SAMPLE_SIZE",
]

DEFAULT_SAMPLE_SIZE = 50

_contract_validator = ContractValidator()


@dataclass(frozen=True, slots=True)
class EvalCorpusBuildReport:
    """Outcome of building one capability's evaluation corpus."""

    capability: str
    candidates: int
    projected: int
    skipped_projection: int
    skipped_validation: int
    written: int
    cases: tuple[dict[str, Any], ...]


def _record_hash(record: Mapping[str, Any]) -> str:
    encoded = json.dumps(record, sort_keys=True, ensure_ascii=True, default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _sample_deterministically(
    records: Sequence[Mapping[str, Any]], sample_size: int
) -> list[Mapping[str, Any]]:
    """Deterministically pick up to ``sample_size`` records.

    Sorted by content hash (not insertion order) so the sample is stable
    across re-runs regardless of upstream generator ordering changes, per
    the repository's determinism principle (`docs/adr/0005-deterministic-ordering.md`).
    """
    ordered = sorted(records, key=_record_hash)
    return ordered[:sample_size]


def build_eval_corpus(
    capability: str,
    records: Sequence[Mapping[str, Any]],
    *,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> EvalCorpusBuildReport:
    """Build the evaluation corpus cases for one capability's training records.

    Args:
        capability: one of :data:`generators.common.contract.adapters.SUPPORTED_CAPABILITIES`.
        records: this capability's already-generated training JSONL records.
        sample_size: maximum number of cases to produce (deterministically sampled).

    Returns:
        A report of how many candidates were considered, projected,
        validated, and ultimately written, plus the case payloads
        themselves (:attr:`EvalCorpusBuildReport.cases`).
    """
    if capability not in SUPPORTED_CAPABILITIES:
        raise ContractAdapterError(
            f"no eval corpus adapter for capability {capability!r}; "
            f"supported: {SUPPORTED_CAPABILITIES}"
        )

    sampled = _sample_deterministically(records, sample_size)

    projected = 0
    skipped_projection = 0
    skipped_validation = 0
    cases: list[dict[str, Any]] = []

    for record in sampled:
        try:
            projection = project_record(capability, record)
        except ContractAdapterError:
            skipped_projection += 1
            continue
        projected += 1

        request_result = _contract_validator.validate_request(projection.request)
        response_result = _contract_validator.validate_response(projection.response)
        if not (request_result.valid and response_result.valid):
            skipped_validation += 1
            continue

        source_hash = None
        metadata = record.get("metadata")
        if isinstance(metadata, Mapping):
            source_hash = metadata.get("protocol_hash")

        cases.append(
            {
                "capability": capability,
                "request": projection.request.model_dump(mode="json"),
                "expected_response": projection.response.model_dump(mode="json"),
                "source_protocol_hash": source_hash,
            }
        )

    return EvalCorpusBuildReport(
        capability=capability,
        candidates=len(sampled),
        projected=projected,
        skipped_projection=skipped_projection,
        skipped_validation=skipped_validation,
        written=len(cases),
        cases=tuple(cases),
    )


class _EvalCorpusStatistics(BaseStatistics):  # type: ignore[misc]
    """Minimal statistics adapter so eval corpus cases can use `DatasetWriter`."""

    def add_sample(self, record: dict[str, Any], json_str: str) -> None:
        class _Record:
            def __init__(self, metadata: dict[str, Any]) -> None:
                self.metadata = metadata

        self._add_base_sample(_Record({"module": record.get("capability", "unknown")}), json_str)


def write_eval_corpus(
    capability: str,
    records: Sequence[Mapping[str, Any]],
    output_dir: Path,
    *,
    sample_size: int = DEFAULT_SAMPLE_SIZE,
) -> EvalCorpusBuildReport:
    """Build and export one capability's eval corpus to ``datasets/``.

    Writes ``<capability>_eval_corpus.jsonl`` plus a manifest and statistics
    file, using the same `DatasetWriter` every other generator uses, so the
    existing validation framework's file-discovery conventions keep working
    unmodified.
    """
    from generators.common.export.writer import DatasetWriter

    report = build_eval_corpus(capability, records, sample_size=sample_size)

    writer: DatasetWriter = DatasetWriter(
        output_dir=output_dir,
        stats=_EvalCorpusStatistics(),
        filename=f"{capability}_eval_corpus.jsonl",
        dataset_name=f"{capability} Evaluation Corpus",
    )
    for case in report.cases:
        writer.write_record(case)

    writer.export_statistics(f"{capability}_eval_corpus_statistics.json")
    writer.export_manifest(f"{capability}_eval_corpus_manifest.json")

    return report
