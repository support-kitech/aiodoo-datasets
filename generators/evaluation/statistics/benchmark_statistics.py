"""Benchmark Statistics for Evaluation Generator."""

from typing import Tuple, Dict
from collections import defaultdict
from types import MappingProxyType
from aiodoo_datasets.generators.evaluation.protocol.domain.benchmark_protocol import EvaluationProtocol

class BenchmarkStatistics:
    """Computes deterministic coverage and distribution statistics."""
    
    @staticmethod
    def compute(dataset: Tuple[EvaluationProtocol, ...]) -> MappingProxyType:
        """Compute coverage and distributions deterministically."""
        
        coverage_by_generator: Dict[str, int] = defaultdict(int)
        coverage_by_protocol: Dict[str, int] = defaultdict(int)
        coverage_by_odoo_version: Dict[str, int] = defaultdict(int)
        coverage_by_module: Dict[str, int] = defaultdict(int)
        coverage_by_suite: Dict[str, int] = defaultdict(int)
        coverage_by_difficulty: Dict[str, int] = defaultdict(int)
        coverage_by_complexity: Dict[str, int] = defaultdict(int)
        
        category_distribution: Dict[str, int] = defaultdict(int)
        type_distribution: Dict[str, int] = defaultdict(int)
        
        for eval_proto in dataset:
            type_distribution[eval_proto.metadata.evaluation_type] += 1
            
            if not eval_proto.catalog:
                continue
                
            catalog_meta = eval_proto.catalog.metadata
            coverage_by_generator[catalog_meta.target_generator] += 1
            category_distribution[catalog_meta.benchmark_category] += 1
            
            for proto in catalog_meta.supported_protocols:
                coverage_by_protocol[proto] += 1
                
            for odoo_v in catalog_meta.supported_odoo_versions:
                coverage_by_odoo_version[odoo_v] += 1
                
            for suite in eval_proto.catalog.suites:
                coverage_by_suite[suite.suite_id] += len(suite.cases)
                for case in suite.cases:
                    coverage_by_module[case.metadata.source_module] += 1
                    coverage_by_difficulty[case.metadata.difficulty] += 1
                    coverage_by_complexity[str(case.metadata.complexity)] += 1
                    
        return MappingProxyType({
            "coverage_by_generator": MappingProxyType(dict(sorted(coverage_by_generator.items()))),
            "coverage_by_protocol": MappingProxyType(dict(sorted(coverage_by_protocol.items()))),
            "coverage_by_odoo_version": MappingProxyType(dict(sorted(coverage_by_odoo_version.items()))),
            "coverage_by_module": MappingProxyType(dict(sorted(coverage_by_module.items()))),
            "coverage_by_suite": MappingProxyType(dict(sorted(coverage_by_suite.items()))),
            "coverage_by_difficulty": MappingProxyType(dict(sorted(coverage_by_difficulty.items()))),
            "coverage_by_complexity": MappingProxyType(dict(sorted(coverage_by_complexity.items()))),
            "category_distribution": MappingProxyType(dict(sorted(category_distribution.items()))),
            "type_distribution": MappingProxyType(dict(sorted(type_distribution.items())))
        })
