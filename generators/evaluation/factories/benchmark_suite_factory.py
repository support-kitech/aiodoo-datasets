"""Benchmark Suite Factory for Evaluation Generator."""

import hashlib
from typing import Tuple
from aiodoo_datasets.generators.evaluation.domain.benchmark_suite import BenchmarkSuite
from aiodoo_datasets.generators.evaluation.domain.evaluation_case import EvaluationCase
from aiodoo_datasets.generators.evaluation.enums import BenchmarkCategory

class BenchmarkSuiteFactory:
    """Factory for creating immutable BenchmarkSuite objects with deterministic IDs."""
    
    @staticmethod
    def generate_id(catalog_id: str, suite_category: BenchmarkCategory) -> str:
        """Generate a deterministic suite ID."""
        category_val = suite_category.value if hasattr(suite_category, 'value') else suite_category
        hash_input = f"SUITE:{catalog_id}:{category_val}"
        suite_hash = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:8]
        return f"SUITE-{suite_hash}"
    
    @staticmethod
    def create(catalog_id: str, suite_category: BenchmarkCategory, suite_name: str, cases: Tuple[EvaluationCase, ...]) -> BenchmarkSuite:
        """Create a new benchmark suite with a hash-based deterministic ID."""
        suite_id = BenchmarkSuiteFactory.generate_id(catalog_id, suite_category)
        
        return BenchmarkSuite(
            suite_id=suite_id,
            suite_name=suite_name,
            cases=cases
        )
