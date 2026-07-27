"""Stable identity helpers for Conversation training records."""

from __future__ import annotations

import hashlib

from generators.conversation.policy import ID_SCHEME_VERSION


def compute_conversation_id(
    module: str,
    anchor_id: str,
    *,
    id_scheme_version: str = ID_SCHEME_VERSION,
) -> str:
    """Deterministic conversation/episode id (no timestamps/UUIDs)."""
    preimage = "\0".join((module.strip(), anchor_id.strip(), id_scheme_version))
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:24]
    return f"CONV-{digest}"


def compute_record_id(
    conversation_id: str,
    turn_index: int,
    *,
    id_scheme_version: str = ID_SCHEME_VERSION,
) -> str:
    """Derive record_id from conversation_id + turn_index + id_scheme_version."""
    preimage = "\0".join((conversation_id.strip(), str(int(turn_index)), id_scheme_version))
    digest = hashlib.sha256(preimage.encode("utf-8")).hexdigest()[:32]
    return f"CNV-{digest}"
