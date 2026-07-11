"""Unit tests for Protocol Manager."""

import unittest

from protocol.core.manager import ProtocolManager
from protocol.domain.enums import ExportFormat
from protocol.pipeline.assembly_options import AssemblyOptions


class DummyInputContext:
    def __init__(self, name: str):
        self.name = name


class TestProtocolManager(unittest.TestCase):

    def test_manager_assemble(self):
        manager = ProtocolManager()
        options = AssemblyOptions()
        result = manager.assemble(DummyInputContext("test_repo"), options)
        
        self.assertIsNotNone(result.protocol_context)
        self.assertTrue(result.validation_result.valid)
        self.assertEqual(result.statistics.objects_created, 7)

    def test_manager_export(self):
        manager = ProtocolManager()
        result = manager.assemble(DummyInputContext("test_repo"), AssemblyOptions())
        
        self.assertIsNotNone(result.protocol_context)
        exported = manager.export(result.protocol_context, ExportFormat.JSON) # type: ignore
        self.assertIsInstance(exported, str)
        self.assertIn("test_repo", exported)
        
    def test_manager_validate(self):
        manager = ProtocolManager()
        result = manager.assemble(DummyInputContext("test_repo"), AssemblyOptions())
        
        self.assertIsNotNone(result.protocol_context)
        val_res = manager.validate(result.protocol_context) # type: ignore
        self.assertTrue(val_res.valid)


if __name__ == "__main__":
    unittest.main()
