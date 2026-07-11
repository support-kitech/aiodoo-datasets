"""Unit tests for Preprocessing Framework domain models."""

import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path

from preprocessing.domain.file import NormalizedFile, DuplicateStatus, Language
from preprocessing.domain.stats import TransformationStatistics


class TestDomainModels(unittest.TestCase):
    """Test immutability and basic properties of domain models."""
    
    def test_normalized_file_immutability(self):
        """Ensure NormalizedFile is frozen."""
        file_node = NormalizedFile(
            file_path=Path("/tmp/foo.py"),
            normalized_path=Path("/foo.py"),
            language=Language.PYTHON,
            raw_content="print( 'hello' )",
            normalized_content="print('hello')",
            duplicate_status=DuplicateStatus.UNIQUE,
        )
        
        with self.assertRaises(FrozenInstanceError):
            file_node.language = "ruby"  # type: ignore

    def test_stats_immutability(self):
        """Ensure TransformationStatistics is frozen."""
        stats = TransformationStatistics()
        
        with self.assertRaises(FrozenInstanceError):
            stats.whitespace_removed_bytes = 10  # type: ignore


if __name__ == "__main__":
    unittest.main()
