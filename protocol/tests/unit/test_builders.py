"""Unit tests for Protocol Framework builders."""

import unittest

from protocol.builders.base import IdentifierFactory
from protocol.builders.metadata_builder import MetadataBuilder
from protocol.builders.reference_builder import ReferenceBuilder
from protocol.builders.relationship_builder import RelationshipBuilder
from protocol.builders.schema_builder import SchemaBuilder
from protocol.builders.manifest_builder import ManifestBuilder
from protocol.builders.dataset_builder import DatasetBuilder
from protocol.builders.context_builder import ContextBuilder
from protocol.domain.enums import (
    ProtocolType,
    ReferenceType,
    RelationshipType,
)
from protocol.domain.version import ProtocolVersion


class TestIdentifierFactory(unittest.TestCase):
    """Test IdentifierFactory determinism."""

    def test_namespaced_ids_differ(self) -> None:
        """Different namespaces produce different identifiers."""
        meta = IdentifierFactory.for_metadata("a")
        ref = IdentifierFactory.for_reference("a")
        self.assertNotEqual(meta, ref)

    def test_same_namespace_deterministic(self) -> None:
        id1 = IdentifierFactory.for_schema("1.0")
        id2 = IdentifierFactory.for_schema("1.0")
        self.assertEqual(id1, id2)


class TestMetadataBuilder(unittest.TestCase):
    def test_build_returns_frozen(self) -> None:
        meta = MetadataBuilder.build({"key": "value"}, identifier_components=("test",))
        self.assertEqual(meta.properties["key"], "value")
        self.assertEqual(meta.protocol_type, ProtocolType.METADATA)
        with self.assertRaises(TypeError):
            meta.properties["x"] = "y"  # type: ignore[index]

    def test_build_deterministic(self) -> None:
        m1 = MetadataBuilder.build({"a": "b"}, identifier_components=("c",))
        m2 = MetadataBuilder.build({"a": "b"}, identifier_components=("c",))
        self.assertEqual(m1.identifier, m2.identifier)


class TestReferenceBuilder(unittest.TestCase):
    def test_build(self) -> None:
        ref = ReferenceBuilder.build(ReferenceType.MODULE, "sale_management")
        self.assertEqual(ref.protocol_type, ProtocolType.REFERENCE)
        self.assertEqual(ref.target_identifier, "sale_management")

    def test_build_deterministic(self) -> None:
        r1 = ReferenceBuilder.build(ReferenceType.FILE, "path/to/file.py")
        r2 = ReferenceBuilder.build(ReferenceType.FILE, "path/to/file.py")
        self.assertEqual(r1.identifier, r2.identifier)


class TestRelationshipBuilder(unittest.TestCase):
    def test_build(self) -> None:
        src = ReferenceBuilder.build(ReferenceType.MODULE, "sale")
        tgt = ReferenceBuilder.build(ReferenceType.MODULE, "account")
        rel = RelationshipBuilder.build(RelationshipType.DEPENDS_ON, src, tgt)
        self.assertEqual(rel.protocol_type, ProtocolType.RELATIONSHIP)
        self.assertIs(rel.source, src)
        self.assertIs(rel.target, tgt)


class TestSchemaBuilder(unittest.TestCase):
    def test_build(self) -> None:
        schema = SchemaBuilder.build("1.0.0", {"type": "object"})
        self.assertEqual(schema.protocol_type, ProtocolType.SCHEMA)
        self.assertEqual(schema.schema_version, "1.0.0")
        self.assertEqual(schema.schema_definition["type"], "object")

    def test_build_none_definition(self) -> None:
        schema = SchemaBuilder.build("2.0.0")
        self.assertEqual(len(schema.schema_definition), 0)


class TestManifestBuilder(unittest.TestCase):
    def _make_version(self) -> ProtocolVersion:
        return ProtocolVersion(
            identifier=IdentifierFactory.for_version("v1"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )

    def test_build(self) -> None:
        ver = self._make_version()
        meta = MetadataBuilder.build({"gen": "planner"}, identifier_components=("m",))
        repo = ReferenceBuilder.build(ReferenceType.REPOSITORY, "enterprise")
        manifest = ManifestBuilder.build(ver, meta, repo)
        self.assertEqual(manifest.protocol_type, ProtocolType.MANIFEST)
        self.assertIs(manifest.version, ver)
        self.assertIsNone(manifest.statistics_reference)
        self.assertEqual(manifest.dependencies, ())


class TestDatasetBuilder(unittest.TestCase):
    def test_build(self) -> None:
        ver = ProtocolVersion(
            identifier=IdentifierFactory.for_version("v1"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        meta = MetadataBuilder.build({}, identifier_components=("x",))
        repo = ReferenceBuilder.build(ReferenceType.REPOSITORY, "r")
        manifest = ManifestBuilder.build(ver, meta, repo)
        schema = SchemaBuilder.build("1.0.0")
        dataset = DatasetBuilder.build(manifest, schema)
        self.assertEqual(dataset.protocol_type, ProtocolType.DATASET)
        self.assertEqual(dataset.items, ())


class TestContextBuilder(unittest.TestCase):
    def test_build_minimal(self) -> None:
        ver = ProtocolVersion(
            identifier=IdentifierFactory.for_version("v"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        meta = MetadataBuilder.build({}, identifier_components=("c",))
        repo = ReferenceBuilder.build(ReferenceType.REPOSITORY, "r")
        manifest = ManifestBuilder.build(ver, meta, repo)
        schema = SchemaBuilder.build("1.0.0")
        dataset = DatasetBuilder.build(manifest, schema)
        ctx = ContextBuilder.build(dataset)
        self.assertEqual(ctx.relationships, ())
        self.assertEqual(ctx.references, ())
        self.assertIs(ctx.dataset, dataset)


if __name__ == "__main__":
    unittest.main()
