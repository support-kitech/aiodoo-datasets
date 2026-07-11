"""Serializer for the Protocol Framework."""

import json
from typing import Any

from protocol.domain.dataset import ProtocolContext, ProtocolDataset
from protocol.domain.identifiers import ProtocolIdentifier
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.metadata import ProtocolMetadata
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship
from protocol.domain.schema import ProtocolSchema
from protocol.domain.version import ProtocolVersion


class Serializer:
    """
    Stateless serializer that converts Protocol domain objects
    into JSON-compatible dictionaries.

    Does not know about files, caches, or persistence.
    Only converts objects to dictionaries and JSON strings.
    """

    @staticmethod
    def identifier_to_dict(identifier: ProtocolIdentifier) -> dict[str, Any]:
        return {"hash_value": identifier.hash_value}

    @staticmethod
    def version_to_dict(version: ProtocolVersion) -> dict[str, Any]:
        return {
            "identifier": Serializer.identifier_to_dict(version.identifier),
            "framework_version": version.framework_version,
            "schema_version": version.schema_version,
            "generator_version": version.generator_version,
        }

    @staticmethod
    def reference_to_dict(ref: ProtocolReference) -> dict[str, Any]:
        return {
            "identifier": Serializer.identifier_to_dict(ref.identifier),
            "reference_type": ref.reference_type.value,
            "target_identifier": ref.target_identifier,
        }

    @staticmethod
    def relationship_to_dict(rel: ProtocolRelationship) -> dict[str, Any]:
        return {
            "identifier": Serializer.identifier_to_dict(rel.identifier),
            "relationship_type": rel.relationship_type.value,
            "source": Serializer.reference_to_dict(rel.source),
            "target": Serializer.reference_to_dict(rel.target),
        }

    @staticmethod
    def metadata_to_dict(metadata: ProtocolMetadata) -> dict[str, Any]:
        return {
            "identifier": Serializer.identifier_to_dict(metadata.identifier),
            "properties": dict(metadata.properties),
        }

    @staticmethod
    def schema_to_dict(schema: ProtocolSchema) -> dict[str, Any]:
        return {
            "identifier": Serializer.identifier_to_dict(schema.identifier),
            "schema_version": schema.schema_version,
            "schema_definition": dict(schema.schema_definition),
        }

    @staticmethod
    def manifest_to_dict(manifest: ProtocolManifest) -> dict[str, Any]:
        result: dict[str, Any] = {
            "identifier": Serializer.identifier_to_dict(manifest.identifier),
            "version": Serializer.version_to_dict(manifest.version),
            "metadata": Serializer.metadata_to_dict(manifest.metadata),
            "repository_reference": Serializer.reference_to_dict(manifest.repository_reference),
            "dependencies": [Serializer.reference_to_dict(d) for d in manifest.dependencies],
        }
        if manifest.statistics_reference is not None:
            result["statistics_reference"] = Serializer.reference_to_dict(
                manifest.statistics_reference
            )
        else:
            result["statistics_reference"] = None
        return result

    @staticmethod
    def dataset_to_dict(dataset: ProtocolDataset) -> dict[str, Any]:
        return {
            "identifier": Serializer.identifier_to_dict(dataset.identifier),
            "manifest": Serializer.manifest_to_dict(dataset.manifest),
            "schema": Serializer.schema_to_dict(dataset.schema),
        }

    @staticmethod
    def context_to_dict(context: ProtocolContext) -> dict[str, Any]:
        return {
            "dataset": Serializer.dataset_to_dict(context.dataset),
            "relationships": [Serializer.relationship_to_dict(r) for r in context.relationships],
            "references": [Serializer.reference_to_dict(r) for r in context.references],
        }

    @staticmethod
    def to_json(context: ProtocolContext) -> str:
        """Serialize a ProtocolContext to a JSON string."""
        return json.dumps(Serializer.context_to_dict(context), indent=2)

    @staticmethod
    def to_jsonl(context: ProtocolContext) -> str:
        """Serialize a ProtocolContext to a single JSONL line."""
        return json.dumps(Serializer.context_to_dict(context))
