"""Unit tests for ProtocolRegistry."""

import unittest

from protocol.domain.enums import ProtocolType, RelationshipType
from protocol.exceptions import ProtocolError
from protocol.registry.registry import ProtocolRegistry


class TestProtocolRegistry(unittest.TestCase):
    def test_register_and_lookup(self) -> None:
        reg = ProtocolRegistry()
        reg.register_protocol_type("dataset", ProtocolType.DATASET)
        reg.register_schema_version("v1", "1.0.0")
        reg.register_relationship_type("depends", RelationshipType.DEPENDS_ON)
        reg.register_export_format("json", "JSON format")
        reg.freeze()

        self.assertEqual(reg.protocol_types["dataset"], ProtocolType.DATASET)
        self.assertEqual(reg.schema_versions["v1"], "1.0.0")
        self.assertEqual(reg.relationship_types["depends"], RelationshipType.DEPENDS_ON)
        self.assertEqual(reg.export_formats["json"], "JSON format")

    def test_freeze_prevents_mutation(self) -> None:
        reg = ProtocolRegistry()
        reg.freeze()
        with self.assertRaises(ProtocolError):
            reg.register_protocol_type("x", ProtocolType.DATASET)
        with self.assertRaises(ProtocolError):
            reg.register_schema_version("x", "1.0")
        with self.assertRaises(ProtocolError):
            reg.register_relationship_type("x", RelationshipType.PARENT)
        with self.assertRaises(ProtocolError):
            reg.register_export_format("x", "desc")

    def test_duplicate_registration_rejected(self) -> None:
        reg = ProtocolRegistry()
        reg.register_protocol_type("ds", ProtocolType.DATASET)
        with self.assertRaises(ProtocolError):
            reg.register_protocol_type("ds", ProtocolType.MANIFEST)

    def test_is_frozen_property(self) -> None:
        reg = ProtocolRegistry()
        self.assertFalse(reg.is_frozen)
        reg.freeze()
        self.assertTrue(reg.is_frozen)

    def test_immutable_views(self) -> None:
        reg = ProtocolRegistry()
        reg.register_export_format("json", "JSON")
        reg.freeze()
        with self.assertRaises(TypeError):
            reg.export_formats["yaml"] = "YAML"  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
