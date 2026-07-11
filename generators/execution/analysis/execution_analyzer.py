"""Execution Analyzer orchestrator."""

from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from aiodoo_datasets.generators.execution.analysis.knowledge.execution_knowledge import (
    ExecutionKnowledge,
)
from aiodoo_datasets.generators.execution.registries.analyzer_registry import AnalyzerRegistry
from typing import Any


class ExecutionAnalyzer:
    """
    Orchestrates the strictly ordered analysis pipeline.
    It holds no business logic of its own.
    """

    def execute(self, context: AnalysisContext) -> ExecutionKnowledge:
        """
        Runs all statically registered analyzers in deterministic order.
        """
        analyzers = AnalyzerRegistry.get_analyzers()
        results: dict[str, Any] = {}

        for analyzer in analyzers:
            result = analyzer.analyze(context)
            # Store results mapped by the class name (in a real implementation this would map precisely)
            results[analyzer.__class__.__name__] = result

        # Assembly of Knowledge object
        return ExecutionKnowledge(
            artifacts=results.get("ArtifactAnalyzer").artifacts
            if "ArtifactAnalyzer" in results
            else (),
            operations=results.get("OperationAnalyzer").operations
            if "OperationAnalyzer" in results
            else (),
            dependencies=results.get("DependencyAnalyzer").dependencies
            if "DependencyAnalyzer" in results
            else (),
            constraints=results.get("ConstraintAnalyzer").constraints
            if "ConstraintAnalyzer" in results
            else (),
            verifications=results.get("VerificationAnalyzer").verifications
            if "VerificationAnalyzer" in results
            else (),
            rollbacks=results.get("RollbackAnalyzer").rollbacks
            if "RollbackAnalyzer" in results
            else (),
        )
