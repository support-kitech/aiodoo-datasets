"""Unit tests for Protocol Pipeline."""

import unittest

from protocol.pipeline.assembly_options import AssemblyOptions
from protocol.pipeline.pipeline import AssemblyPipeline
from protocol.pipeline.pipeline_context import PipelineContext
from protocol.registry.registry import ProtocolRegistry


class DummyInputContext:
    def __init__(self, name: str):
        self.name = name


class TestPipeline(unittest.TestCase):

    def test_pipeline_assemble(self):
        pipeline = AssemblyPipeline()
        registry = ProtocolRegistry()
        registry.freeze()
        options = AssemblyOptions()
        
        ctx = PipelineContext(
            input_context=DummyInputContext("test_repo"),
            options=options,
            registry=registry
        )
        
        result = pipeline.assemble(ctx)
        self.assertIsNotNone(result.protocol_context)
        self.assertTrue(result.validation_result.valid)
        self.assertEqual(result.statistics.objects_created, 7)
        self.assertIsNotNone(result.export_payload)

    def test_pipeline_no_export(self):
        pipeline = AssemblyPipeline()
        registry = ProtocolRegistry()
        registry.freeze()
        options = AssemblyOptions(export_format="")
        
        ctx = PipelineContext(
            input_context=DummyInputContext("test_repo"),
            options=options,
            registry=registry
        )
        
        result = pipeline.assemble(ctx)
        self.assertIsNotNone(result.protocol_context)
        self.assertTrue(result.validation_result.valid)
        self.assertIsNone(result.export_payload)


if __name__ == "__main__":
    unittest.main()
