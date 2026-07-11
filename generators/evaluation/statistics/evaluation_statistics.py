"""Evaluation Statistics for Evaluation Generator."""

from typing import Tuple
from types import MappingProxyType
from aiodoo_datasets.generators.evaluation.protocol.domain.benchmark_protocol import EvaluationProtocol

class EvaluationStatistics:
    """Computes deterministic aggregates for the entire evaluation dataset."""
    
    @staticmethod
    def compute(dataset: Tuple[EvaluationProtocol, ...]) -> MappingProxyType:
        """Compute total counts across the dataset."""
        total_evaluations = len(dataset)
        total_catalogs = 0
        total_suites = 0
        total_cases = 0
        total_rules = 0
        total_references = 0
        total_expected_outputs = 0
        total_ground_truths = 0
        
        for eval_proto in dataset:
            if eval_proto.catalog:
                total_catalogs += 1
                for suite in eval_proto.catalog.suites:
                    total_suites += 1
                    for case in suite.cases:
                        total_cases += 1
                        total_rules += len(case.rules)
                        total_references += len(case.references)
                        
                        if case.expected_output:
                            total_expected_outputs += 1
                        if case.ground_truth:
                            total_ground_truths += 1
                            
        return MappingProxyType({
            "total_evaluations": total_evaluations,
            "total_catalogs": total_catalogs,
            "total_suites": total_suites,
            "total_cases": total_cases,
            "total_rules": total_rules,
            "total_references": total_references,
            "total_expected_outputs": total_expected_outputs,
            "total_ground_truths": total_ground_truths
        })
