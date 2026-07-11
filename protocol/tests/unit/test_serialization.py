"""Unit tests for Protocol serialization, deserialization, and export."""

import json
import unittest

from protocol.builders.base import IdentifierFactory
from protocol.builders.context_builder import ContextBuilder
from protocol.builders.dataset_builder import DatasetBuilder
from protocol.builders.manifest_builder import ManifestBuilder
from protocol.builders.metadata_builder import MetadataBuilder
from protocol.builders.reference_builder import ReferenceBuilder
from protocol.builders.relationship_builder import RelationshipBuilder
from protocol.builders.schema_builder import SchemaBuilder
from protocol.domain.enums import ReferenceType, RelationshipType, ExportFormat
from protocol.domain.version import ProtocolVersion
from protocol.serialization.deserializer import Deserializer
from protocol.serialization.exporter import Exporter
from protocol.serialization.serializer import Serializer


def _make_context():
    """Helper that builds a full ProtocolContext graph."""
    ver = ProtocolVersion(
        identifier=IdentifierFactory.for_version("v1"),
        framework_version="1.0.0",
        schema_version="1.0.0",
        generator_version="1.0.0",
    )
    meta = MetadataBuilder.build(
        {"generator": "planner", "language": "python"},
        identifier_components=("meta",),
    )
    repo = ReferenceBuilder.build(ReferenceType.REPOSITORY, "enterprise")
    manifest = ManifestBuilder.build(ver, meta, repo)
    schema = SchemaBuilder.build("1.0.0")
    dataset = DatasetBuilder.build(manifest, schema)

    src = ReferenceBuilder.build(ReferenceType.MODULE, "sale")
    tgt = ReferenceBuilder.build(ReferenceType.MODULE, "account")
    rel = RelationshipBuilder.build(RelationshipType.DEPENDS_ON, src, tgt)

    return ContextBuilder.build(dataset, relationships=(rel,), references=(src, tgt))


class TestSerializer(unittest.TestCase):

    def test_to_dict(self) -> None:
        ctx = _make_context()
        d = Serializer.context_to_dict(ctx)
        self.assertIn("dataset", d)
        self.assertIn("relationships", d)
        self.assertIn("references", d)
        self.assertEqual(len(d["relationships"]), 1)
        self.assertEqual(len(d["references"]), 2)

    def test_to_json(self) -> None:
        ctx = _make_context()
        j = Serializer.to_json(ctx)
        parsed = json.loads(j)
        self.assertIn("dataset", parsed)

    def test_to_jsonl(self) -> None:
        ctx = _make_context()
        line = Serializer.to_jsonl(ctx)
        parsed = json.loads(line)
        self.assertIn("dataset", parsed)


class TestDeserializer(unittest.TestCase):

    def test_from_json_roundtrip(self) -> None:
        """Serialize then deserialize — structural equality."""
        original = _make_context()
        j = Serializer.to_json(original)
        restored = Deserializer.from_json(j)

        self.assertEqual(
            original.dataset.identifier.hash_value,
            restored.dataset.identifier.hash_value,
        )
        self.assertEqual(
            original.dataset.manifest.metadata.properties["generator"],
            restored.dataset.manifest.metadata.properties["generator"],
        )
        self.assertEqual(len(original.relationships), len(restored.relationships))
        self.assertEqual(len(original.references), len(restored.references))

    def test_from_jsonl_roundtrip(self) -> None:
        original = _make_context()
        line = Serializer.to_jsonl(original)
        restored = Deserializer.from_jsonl(line)
        self.assertEqual(
            original.dataset.identifier.hash_value,
            restored.dataset.identifier.hash_value,
        )

    def test_restored_metadata_immutable(self) -> None:
        ctx = _make_context()
        j = Serializer.to_json(ctx)
        restored = Deserializer.from_json(j)
        with self.assertRaises(TypeError):
            restored.dataset.manifest.metadata.properties["x"] = "y"  # type: ignore[index]


class TestExporter(unittest.TestCase):

    def test_export_json(self) -> None:
        ctx = _make_context()
        result = Exporter.export(ctx, ExportFormat.JSON)
        self.assertIsInstance(result, str)
        parsed = json.loads(result)  # type: ignore[arg-type]
        self.assertIn("dataset", parsed)

    def test_export_jsonl(self) -> None:
        ctx = _make_context()
        result = Exporter.export(ctx, ExportFormat.JSONL)
        self.assertIsInstance(result, str)

    def test_export_dict(self) -> None:
        ctx = _make_context()
        result = Exporter.export(ctx, ExportFormat.DICT)
        self.assertIsInstance(result, dict)

    def test_export_unsupported_format(self) -> None:
        ctx = _make_context()
        with self.assertRaises(ValueError):
            Exporter.export(ctx, "xml") # type: ignore


if __name__ == "__main__":
    unittest.main()
