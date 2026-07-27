"""Subject partitioning for Approval generation (one subject = one decision)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from generators.approval.identity import compute_record_id
from generators.approval.policy import CAPABILITY_DATA_KEYS, ID_SCHEME_VERSION


@dataclass(frozen=True, slots=True)
class ApprovalSubject:
    """One reviewable upstream artifact (planner/coding/repair/execution row)."""

    capability: str
    data_key: str
    subject_id: str
    source_object_id: str
    record_id: str
    module: str
    source_record: Mapping[str, Any]

    @property
    def subject_label(self) -> str:
        return f"Approve {self.capability} artifact {self.source_object_id} ({self.module})"


class SubjectPartitioner:
    """Extract deterministic Approval subjects from upstream protocol records."""

    @staticmethod
    def extract(
        input_protocols: Mapping[str, Any],
        *,
        id_scheme_version: str = ID_SCHEME_VERSION,
    ) -> tuple[ApprovalSubject, ...]:
        """Return unique subjects sorted by record_id."""
        subjects: list[ApprovalSubject] = []
        seen_ids: set[str] = set()

        for capability, data_key in CAPABILITY_DATA_KEYS:
            raw = input_protocols.get(data_key)
            records = _as_record_sequence(raw)
            for record in records:
                if not isinstance(record, Mapping):
                    continue
                source_object_id = _source_object_id(capability, record)
                module = _module_name(record)
                subject_id = f"{capability}:{module}:{source_object_id}"
                record_id = compute_record_id(
                    capability,
                    subject_id,
                    source_object_id,
                    id_scheme_version=id_scheme_version,
                )
                if record_id in seen_ids:
                    continue
                seen_ids.add(record_id)
                subjects.append(
                    ApprovalSubject(
                        capability=capability,
                        data_key=data_key,
                        subject_id=subject_id,
                        source_object_id=source_object_id,
                        record_id=record_id,
                        module=module,
                        source_record=record,
                    )
                )

        subjects.sort(key=lambda s: s.record_id)
        return tuple(subjects)


def _as_record_sequence(raw: Any) -> Sequence[Any]:
    if raw is None:
        return ()
    if isinstance(raw, Mapping):
        # Single legacy blob — treat as one record only if it looks like a train row.
        if "metadata" in raw or "output" in raw or "instruction" in raw:
            return (raw,)
        return ()
    if isinstance(raw, (list, tuple)):
        return raw
    return ()


def _module_name(record: Mapping[str, Any]) -> str:
    meta = record.get("metadata")
    if isinstance(meta, Mapping):
        module = meta.get("module") or meta.get("source_module")
        if isinstance(module, str) and module.strip():
            return module.strip()
    return "unknown"


def _source_object_id(capability: str, record: Mapping[str, Any]) -> str:
    meta = record.get("metadata") if isinstance(record.get("metadata"), Mapping) else {}
    output = record.get("output") if isinstance(record.get("output"), Mapping) else {}

    if capability == "execution":
        execution_id = output.get("execution_id")
        if isinstance(execution_id, str) and execution_id.strip():
            return execution_id.strip()

    protocol_hash = meta.get("protocol_hash")
    if isinstance(protocol_hash, str) and protocol_hash.strip():
        return protocol_hash.strip()

    module_hash = meta.get("module_hash")
    if isinstance(module_hash, str) and module_hash.strip():
        return module_hash.strip()

    module = _module_name(record)
    instruction = record.get("instruction")
    instruction_s = instruction.strip() if isinstance(instruction, str) else ""
    preimage = f"{capability}:{module}:{instruction_s}"
    return hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:16]
