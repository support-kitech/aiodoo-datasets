"""Unit tests for Phase 2 Processors & Builders."""

import unittest
from pathlib import Path

from preprocessing.domain.file import Language
from preprocessing.processors.base import ProcessorContext
from preprocessing.processors.registry import ProcessorRegistry
from preprocessing.processors.pipeline import ProcessorPipeline
from preprocessing.processors.text.whitespace import WhitespaceProcessor
from preprocessing.processors.analysis.duplicate import DuplicateProcessor
from preprocessing.processors.metadata.metadata import MetadataProcessor


class TestPhase2(unittest.TestCase):
    """Test processors and pipelines."""
    
    def setUp(self):
        self.registry = ProcessorRegistry()
        self.registry.register_universal(WhitespaceProcessor())
        self.registry.register_analysis(DuplicateProcessor())
        self.registry.register_analysis(MetadataProcessor())
        self.pipeline = ProcessorPipeline(self.registry)
        
    def test_whitespace_processor(self):
        """Test trailing whitespace removal."""
        ctx = ProcessorContext(
            file_path=Path("test.py"),
            normalized_path=Path("test.py"),
            language=Language.PYTHON,
            raw_content="def test():   \n    pass  ",
            current_content="def test():   \n    pass  "
        )
        
        processor = WhitespaceProcessor()
        new_ctx = processor.process(ctx)
        
        self.assertEqual(new_ctx.current_content, "def test():\n    pass")
        self.assertGreater(new_ctx.statistics.whitespace_removed_bytes, 0)
        
    def test_pipeline_execution(self):
        """Test full pipeline execution."""
        ctx1 = ProcessorContext(
            file_path=Path("test1.py"),
            normalized_path=Path("test1.py"),
            language=Language.PYTHON,
            raw_content="print('hello')  ",
            current_content="print('hello')  "
        )
        
        final_ctx1 = self.pipeline.execute(ctx1)
        self.assertEqual(final_ctx1.current_content, "print('hello')")
        self.assertEqual(final_ctx1.metadata.get("duplicate_status"), "UNIQUE")
        self.assertTrue(final_ctx1.metadata.get("processed_by_framework"))
        
        # Test duplicate processing
        ctx2 = ProcessorContext(
            file_path=Path("test2.py"),
            normalized_path=Path("test2.py"),
            language=Language.PYTHON,
            raw_content="print('hello')  ",
            current_content="print('hello')  "
        )
        final_ctx2 = self.pipeline.execute(ctx2)
        self.assertEqual(final_ctx2.metadata.get("duplicate_status"), "DUPLICATE")

if __name__ == "__main__":
    unittest.main()
