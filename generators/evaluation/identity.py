"""Stable identity helpers for Evaluation training records."""

from __future__ import annotations

import hashlib

from generators.evaluation.policy import ID_SCHEME_VERSION


def compute_candidate_id(capability: str, source_object_id: str) -> str:
    """Stable candidate identity for one upstream artifact under test."""
    preimage = "\0".join((capability.strip(), source_object_id.strip()))
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:24]
    return f"CAND-{digest}"


def compute_record_id(
    candidate_id: str,
    evaluation_case_key: str,
    *,
    id_scheme_version: str = ID_SCHEME_VERSION,
) -> str:
    """Derive record_id from candidate_id + evaluation_case_key + scheme."""
    preimage = "\0".join((candidate_id.strip(), evaluation_case_key.strip(), id_scheme_version))
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:32]
    return f"EVL-{digest}"
