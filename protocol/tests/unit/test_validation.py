"""Unit tests for Protocol structural validators."""

import unittest

from protocol.builders.base import IdentifierFactory
from protocol.builders.metadata_builder import MetadataBuilder
from protocol.builders.reference_builder import ReferenceBuilder
from protocol.builders.relationship_builder import RelationshipBuilder
from protocol.builders.schema_builder import SchemaBuilder
from protocol.builders.manifest_builder import ManifestBuilder
from protocol.builders.dataset_builder import DatasetBuilder
from protocol.domain.enums import ReferenceType, RelationshipType
from protocol.domain.identifiers import ProtocolIdentifier
from protocol.domain.references import ProtocolReference
from protocol.domain.relationships import ProtocolRelationship
from protocol.domain.version import ProtocolVersion
from protocol.validation.metadata_validator import MetadataValidator
from protocol.validation.reference_validator import ReferenceValidator
from protocol.validation.relationship_validator import RelationshipValidator
from protocol.validation.schema_validator import SchemaValidator
from protocol.validation.manifest_validator import ManifestValidator
from protocol.validation.dataset_validator import DatasetValidator
from protocol.validation.base import ValidationResult


class TestValidationResult(unittest.TestCase):
    def test_success(self) -> None:
        r = ValidationResult.success()
        self.assertTrue(r.valid)
        self.assertEqual(r.errors, ())

    def test_failure(self) -> None:
        r = ValidationResult.failure("bad", "worse")
        self.assertFalse(r.valid)
        self.assertEqual(r.errors, ("bad", "worse"))

    def test_merge(self) -> None:
        ok = ValidationResult.success()
        bad = ValidationResult.failure("err")
        merged = ok.merge(bad)
        self.assertFalse(merged.valid)
        self.assertEqual(merged.errors, ("err",))

    def test_immutable(self) -> None:
        r = ValidationResult.success()
        with self.assertRaises(AttributeError):
            r.valid = False  # type: ignore[misc]


class TestMetadataValidator(unittest.TestCase):
    def test_valid(self) -> None:
        meta = MetadataBuilder.build({"k": "v"}, identifier_components=("t",))
        self.assertTrue(MetadataValidator.validate(meta).valid)


class TestReferenceValidator(unittest.TestCase):
    def test_valid(self) -> None:
        ref = ReferenceBuilder.build(ReferenceType.MODULE, "sale")
        self.assertTrue(ReferenceValidator.validate(ref).valid)

    def test_empty_target(self) -> None:
        ref = ProtocolReference(
            identifier=ProtocolIdentifier.generate("x"),
            reference_type=ReferenceType.FILE,
            target_identifier="",
        )
        result = ReferenceValidator.validate(ref)
        self.assertFalse(result.valid)
        self.assertIn("target_identifier must not be empty", result.errors[0])


class TestRelationshipValidator(unittest.TestCase):
    def test_valid(self) -> None:
        src = ReferenceBuilder.build(ReferenceType.MODULE, "sale")
        tgt = ReferenceBuilder.build(ReferenceType.MODULE, "account")
        rel = RelationshipBuilder.build(RelationshipType.DEPENDS_ON, src, tgt)
        self.assertTrue(RelationshipValidator.validate(rel).valid)

    def test_self_referencing(self) -> None:
        ref = ReferenceBuilder.build(ReferenceType.MODULE, "sale")
        rel = ProtocolRelationship(
            identifier=ProtocolIdentifier.generate("self"),
            relationship_type=RelationshipType.PARENT,
            source=ref,
            target=ref,
        )
        result = RelationshipValidator.validate(rel)
        self.assertFalse(result.valid)


class TestSchemaValidator(unittest.TestCase):
    def test_valid(self) -> None:
        schema = SchemaBuilder.build("1.0.0")
        self.assertTrue(SchemaValidator.validate(schema).valid)


class TestManifestValidator(unittest.TestCase):
    def test_valid(self) -> None:
        ver = ProtocolVersion(
            identifier=IdentifierFactory.for_version("v1"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        meta = MetadataBuilder.build({}, identifier_components=("m",))
        repo = ReferenceBuilder.build(ReferenceType.REPOSITORY, "r")
        manifest = ManifestBuilder.build(ver, meta, repo)
        self.assertTrue(ManifestValidator.validate(manifest).valid)


class TestDatasetValidator(unittest.TestCase):
    def test_valid(self) -> None:
        ver = ProtocolVersion(
            identifier=IdentifierFactory.for_version("v1"),
            framework_version="1.0.0",
            schema_version="1.0.0",
            generator_version="1.0.0",
        )
        meta = MetadataBuilder.build({}, identifier_components=("m",))
        repo = ReferenceBuilder.build(ReferenceType.REPOSITORY, "r")
        manifest = ManifestBuilder.build(ver, meta, repo)
        schema = SchemaBuilder.build("1.0.0")
        dataset = DatasetBuilder.build(manifest, schema)
        self.assertTrue(DatasetValidator.validate(dataset).valid)


if __name__ == "__main__":
    unittest.main()
