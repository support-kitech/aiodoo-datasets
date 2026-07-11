"""Unit tests for Protocol Framework domain models."""

import unittest
from types import MappingProxyType

from protocol.domain.identifiers import ProtocolIdentifier
from protocol.domain.enums import ProtocolType, ReferenceType, RelationshipType
from protocol.domain.version import ProtocolVersion
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship
from protocol.domain.metadata import ProtocolMetadata
from protocol.domain.schema import ProtocolSchema
from protocol.domain.manifest import ProtocolManifest
from protocol.domain.dataset import ProtocolDataset, ProtocolContext


class TestProtocolIdentifier(unittest.TestCase):
    """Test deterministic identifier generation."""

    def test_generate_deterministic(self) -> None:
        """Same inputs always produce the same hash."""
        id1 = ProtocolIdentifier.generate("repo", "module", "file.py")
        id2 = ProtocolIdentifier.generate("repo", "module", "file.py")
        self.assertEqual(id1, id2)

    def test_generate_different_inputs(self) -> None:
        """Different inputs produce different hashes."""
        id1 = ProtocolIdentifier.generate("repo", "module_a")
        id2 = ProtocolIdentifier.generate("repo", "module_b")
        self.assertNotEqual(id1, id2)

    def test_separator_prevents_collision(self) -> None:
        """("ab", "c") must differ from ("a", "bc")."""
        id1 = ProtocolIdentifier.generate("ab", "c")
        id2 = ProtocolIdentifier.generate("a", "bc")
        self.assertNotEqual(id1, id2)

    def test_str_returns_hash(self) -> None:
        pid = ProtocolIdentifier.generate("test")
        self.assertEqual(str(pid), pid.hash_value)

    def test_immutable(self) -> None:
        pid = ProtocolIdentifier.generate("test")
        with self.assertRaises(AttributeError):
            pid.hash_value = "mutated"  # type: ignore[misc]


class TestProtocolVersion(unittest.TestCase):
    """Test ProtocolVersion domain model."""

    def test_construction(self) -> None:
        pid = ProtocolIdentifier.generate("ver")
        ver = ProtocolVersion(
            identifier=pid,
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        self.assertEqual(ver.protocol_type, ProtocolType.VERSION)
        self.assertEqual(ver.framework_version, "1.0.0")

    def test_immutable(self) -> None:
        pid = ProtocolIdentifier.generate("ver")
        ver = ProtocolVersion(
            identifier=pid,
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        with self.assertRaises(AttributeError):
            ver.framework_version = "2.0.0"  # type: ignore[misc]


class TestProtocolReference(unittest.TestCase):
    """Test ProtocolReference domain model."""

    def test_construction(self) -> None:
        pid = ProtocolIdentifier.generate("ref")
        ref = ProtocolReference(
            identifier=pid,
            reference_type=ReferenceType.MODULE,
            target_identifier="sale_management",
        )
        self.assertEqual(ref.protocol_type, ProtocolType.REFERENCE)
        self.assertEqual(ref.reference_type, ReferenceType.MODULE)
        self.assertEqual(ref.target_identifier, "sale_management")


class TestProtocolRelationship(unittest.TestCase):
    """Test ProtocolRelationship domain model."""

    def test_directed_edge(self) -> None:
        src = ProtocolReference(
            identifier=ProtocolIdentifier.generate("src"),
            reference_type=ReferenceType.MODULE,
            target_identifier="sale",
        )
        tgt = ProtocolReference(
            identifier=ProtocolIdentifier.generate("tgt"),
            reference_type=ReferenceType.MODULE,
            target_identifier="account",
        )
        rel = ProtocolRelationship(
            identifier=ProtocolIdentifier.generate("rel"),
            relationship_type=RelationshipType.DEPENDS_ON,
            source=src,
            target=tgt,
        )
        self.assertEqual(rel.protocol_type, ProtocolType.RELATIONSHIP)
        self.assertEqual(rel.relationship_type, RelationshipType.DEPENDS_ON)
        self.assertIs(rel.source, src)
        self.assertIs(rel.target, tgt)


class TestProtocolMetadata(unittest.TestCase):
    """Test ProtocolMetadata domain model."""

    def test_default_empty_properties(self) -> None:
        pid = ProtocolIdentifier.generate("meta")
        meta = ProtocolMetadata(identifier=pid)
        self.assertEqual(len(meta.properties), 0)
        self.assertEqual(meta.protocol_type, ProtocolType.METADATA)

    def test_properties_immutable(self) -> None:
        pid = ProtocolIdentifier.generate("meta")
        props = MappingProxyType({"generator": "planner", "language": "python"})
        meta = ProtocolMetadata(identifier=pid, properties=props)
        self.assertEqual(meta.properties["generator"], "planner")
        with self.assertRaises(TypeError):
            meta.properties["new_key"] = "fail"  # type: ignore[index]


class TestProtocolSchema(unittest.TestCase):
    """Test ProtocolSchema domain model."""

    def test_construction(self) -> None:
        pid = ProtocolIdentifier.generate("schema")
        schema = ProtocolSchema(
            identifier=pid,
            schema_version="1.0.0",
        )
        self.assertEqual(schema.protocol_type, ProtocolType.SCHEMA)
        self.assertEqual(schema.schema_version, "1.0.0")


class TestProtocolManifest(unittest.TestCase):
    """Test ProtocolManifest domain model."""

    def _make_manifest(self) -> ProtocolManifest:
        ver = ProtocolVersion(
            identifier=ProtocolIdentifier.generate("ver"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        meta = ProtocolMetadata(
            identifier=ProtocolIdentifier.generate("meta"),
            properties=MappingProxyType({"generator": "planner"}),
        )
        repo_ref = ProtocolReference(
            identifier=ProtocolIdentifier.generate("repo"),
            reference_type=ReferenceType.REPOSITORY,
            target_identifier="enterprise",
        )
        return ProtocolManifest(
            identifier=ProtocolIdentifier.generate("manifest"),
            version=ver,
            metadata=meta,
            repository_reference=repo_ref,
        )

    def test_construction(self) -> None:
        m = self._make_manifest()
        self.assertEqual(m.protocol_type, ProtocolType.MANIFEST)
        self.assertEqual(m.dependencies, ())
        self.assertIsNone(m.statistics_reference)

    def test_immutable(self) -> None:
        m = self._make_manifest()
        with self.assertRaises(AttributeError):
            m.version = None  # type: ignore[misc]


class TestProtocolDatasetAndContext(unittest.TestCase):
    """Test ProtocolDataset and ProtocolContext domain models."""

    def _make_context(self) -> ProtocolContext:
        ver = ProtocolVersion(
            identifier=ProtocolIdentifier.generate("ver"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        meta = ProtocolMetadata(identifier=ProtocolIdentifier.generate("meta"))
        repo_ref = ProtocolReference(
            identifier=ProtocolIdentifier.generate("repo"),
            reference_type=ReferenceType.REPOSITORY,
            target_identifier="enterprise",
        )
        manifest = ProtocolManifest(
            identifier=ProtocolIdentifier.generate("manifest"),
            version=ver,
            metadata=meta,
            repository_reference=repo_ref,
        )
        schema = ProtocolSchema(
            identifier=ProtocolIdentifier.generate("schema"),
            schema_version="1.0.0",
        )
        dataset = ProtocolDataset(
            identifier=ProtocolIdentifier.generate("dataset"),
            manifest=manifest,
            schema=schema,
        )
        return ProtocolContext(dataset=dataset)

    def test_construction(self) -> None:
        ctx = self._make_context()
        self.assertEqual(ctx.dataset.protocol_type, ProtocolType.DATASET)
        self.assertEqual(ctx.relationships, ())
        self.assertEqual(ctx.references, ())

    def test_dataset_immutable(self) -> None:
        ctx = self._make_context()
        with self.assertRaises(AttributeError):
            ctx.dataset = None  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
