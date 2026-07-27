"""Stable identity helpers for Approval training records."""

from __future__ import annotations

import hashlib

from generators.approval.policy import ID_SCHEME_VERSION


def compute_record_id(
    capability: str,
    subject_id: str,
    source_object_id: str,
    *,
    id_scheme_version: str = ID_SCHEME_VERSION,
) -> str:
    """Derive a deterministic Approval record_id.

    Preimage (Step 2.1)::

        capability + subject_id + source_object_id + id_scheme_version

    No timestamps, UUIDs, or randomness.
    """
    preimage = "\0".join(
        (capability.strip(), subject_id.strip(), source_object_id.strip(), id_scheme_version)
    )
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:32]
    return f"APR-{digest}"
