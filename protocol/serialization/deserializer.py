"""Deserializer for the Protocol Framework."""

import json
from types import MappingProxyType
from typing import Any

from protocol.domain.dataset import ProtocolContext, ProtocolDataset
from protocol.domain.enums import ReferenceType, RelationshipType
from protocol.domain.identifiers import ProtocolIdentifier
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.metadata import ProtocolMetadata
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship
from protocol.domain.schema import ProtocolSchema
from protocol.domain.version import ProtocolVersion


class Deserializer:
    """
    Stateless deserializer that hydrates Protocol domain objects
    from JSON-compatible dictionaries.

    Does not know about files, caches, or persistence.
    Only converts dictionaries and JSON strings to objects.
    """

    @staticmethod
    def identifier_from_dict(data: dict[str, Any]) -> ProtocolIdentifier:
        return ProtocolIdentifier(hash_value=data["hash_value"])

    @staticmethod
    def version_from_dict(data: dict[str, Any]) -> ProtocolVersion:
        return ProtocolVersion(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            framework_version=data["framework_version"],
            schema_version=data["schema_version"],
            generator_version=data["generator_version"],
        )

    @staticmethod
    def reference_from_dict(data: dict[str, Any]) -> ProtocolReference:
        return ProtocolReference(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            reference_type=ReferenceType(data["reference_type"]),
            target_identifier=data["target_identifier"],
        )

    @staticmethod
    def relationship_from_dict(data: dict[str, Any]) -> ProtocolRelationship:
        return ProtocolRelationship(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            relationship_type=RelationshipType(data["relationship_type"]),
            source=Deserializer.reference_from_dict(data["source"]),
            target=Deserializer.reference_from_dict(data["target"]),
        )

    @staticmethod
    def metadata_from_dict(data: dict[str, Any]) -> ProtocolMetadata:
        return ProtocolMetadata(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            properties=MappingProxyType(data.get("properties", {})),
        )

    @staticmethod
    def schema_from_dict(data: dict[str, Any]) -> ProtocolSchema:
        return ProtocolSchema(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            schema_version=data["schema_version"],
            schema_definition=MappingProxyType(data.get("schema_definition", {})),
        )

    @staticmethod
    def manifest_from_dict(data: dict[str, Any]) -> ProtocolManifest:
        stats_ref = None
        if data.get("statistics_reference") is not None:
            stats_ref = Deserializer.reference_from_dict(data["statistics_reference"])

        deps = tuple(
            Deserializer.reference_from_dict(d) for d in data.get("dependencies", [])
        )

        return ProtocolManifest(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            version=Deserializer.version_from_dict(data["version"]),
            metadata=Deserializer.metadata_from_dict(data["metadata"]),
            repository_reference=Deserializer.reference_from_dict(data["repository_reference"]),
            statistics_reference=stats_ref,
            dependencies=deps,
        )

    @staticmethod
    def dataset_from_dict(data: dict[str, Any]) -> ProtocolDataset:
        return ProtocolDataset(
            identifier=Deserializer.identifier_from_dict(data["identifier"]),
            manifest=Deserializer.manifest_from_dict(data["manifest"]),
            schema=Deserializer.schema_from_dict(data["schema"]),
        )

    @staticmethod
    def context_from_dict(data: dict[str, Any]) -> ProtocolContext:
        relationships = tuple(
            Deserializer.relationship_from_dict(r) for r in data.get("relationships", [])
        )
        references = tuple(
            Deserializer.reference_from_dict(r) for r in data.get("references", [])
        )
        return ProtocolContext(
            dataset=Deserializer.dataset_from_dict(data["dataset"]),
            relationships=relationships,
            references=references,
        )

    @staticmethod
    def from_json(json_str: str) -> ProtocolContext:
        """Deserialize a JSON string to a ProtocolContext."""
        data = json.loads(json_str)
        return Deserializer.context_from_dict(data)

    @staticmethod
    def from_jsonl(jsonl_line: str) -> ProtocolContext:
        """Deserialize a single JSONL line to a ProtocolContext."""
        data = json.loads(jsonl_line)
        return Deserializer.context_from_dict(data)
