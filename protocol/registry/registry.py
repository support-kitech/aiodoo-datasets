"""ProtocolRegistry for the Protocol Framework."""

import hashlib
from types import MappingProxyType
from typing import Any, Mapping

from protocol.domain.enums import ProtocolType, RelationshipType
from protocol.exceptions import ProtocolError


class ProtocolRegistry:
    """
    A freezable registry tracking known protocol types, schema versions,
    relationship types, and export formats.

    Lifecycle:
        Create -> Register -> Freeze -> Lookup Only

    After freeze, any mutation attempt raises ProtocolError.
    """

    def __init__(self) -> None:
        self._frozen = False
        self._protocol_types: dict[str, ProtocolType] = {}
        self._schema_versions: dict[str, str] = {}
        self._relationship_types: dict[str, RelationshipType] = {}
        self._export_formats: dict[str, str] = {}
        self._metadata: dict[str, Any] = {}

    # ── Mutation Guard ────────────────────────────────────

    def _assert_mutable(self) -> None:
        """Raise if the registry has been frozen."""
        if self._frozen:
            raise ProtocolError("Cannot mutate a frozen ProtocolRegistry.")

    # ── Registration ──────────────────────────────────────

    def register_protocol_type(self, name: str, protocol_type: ProtocolType) -> None:
        """Register a named protocol type."""
        self._assert_mutable()
        if name in self._protocol_types:
            raise ProtocolError(f"Duplicate protocol type registration: {name}")
        self._protocol_types[name] = protocol_type

    def register_schema_version(self, name: str, version: str) -> None:
        """Register a named schema version."""
        self._assert_mutable()
        if name in self._schema_versions:
            raise ProtocolError(f"Duplicate schema version registration: {name}")
        self._schema_versions[name] = version

    def register_relationship_type(self, name: str, rel_type: RelationshipType) -> None:
        """Register a named relationship type."""
        self._assert_mutable()
        if name in self._relationship_types:
            raise ProtocolError(f"Duplicate relationship type registration: {name}")
        self._relationship_types[name] = rel_type

    def register_export_format(self, name: str, description: str) -> None:
        """Register a named export format."""
        self._assert_mutable()
        if name in self._export_formats:
            raise ProtocolError(f"Duplicate export format registration: {name}")
        self._export_formats[name] = description

    # ── Freeze ────────────────────────────────────────────

    def freeze(self) -> None:
        """
        Freeze the registry. After this call, no further mutations
        are permitted; only lookups are allowed.
        """
        self._frozen = True

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    @property
    def hash_value(self) -> str:
        """
        Compute a deterministic SHA-256 hash of the registry contents.
        Useful for consistency, debugging, and compatibility verification.
        """
        sha256 = hashlib.sha256()

        def _update(prefix: str, d: dict) -> None:
            for k, v in sorted(d.items()):
                val_str = str(getattr(v, "value", v))
                sha256.update(f"{prefix}:{k}:{val_str}".encode("utf-8"))
                sha256.update(b"\x00")

        _update("protocol_type", self._protocol_types)
        _update("schema_version", self._schema_versions)
        _update("relationship_type", self._relationship_types)
        _update("export_format", self._export_formats)

        return sha256.hexdigest()

    # ── Lookups (immutable views) ─────────────────────────

    @property
    def protocol_types(self) -> Mapping[str, ProtocolType]:
        return MappingProxyType(self._protocol_types)

    @property
    def schema_versions(self) -> Mapping[str, str]:
        return MappingProxyType(self._schema_versions)

    @property
    def relationship_types(self) -> Mapping[str, RelationshipType]:
        return MappingProxyType(self._relationship_types)

    @property
    def export_formats(self) -> Mapping[str, str]:
        return MappingProxyType(self._export_formats)
