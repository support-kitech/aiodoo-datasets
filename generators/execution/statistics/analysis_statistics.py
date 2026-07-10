"""Statistics collector for the analysis phase."""

from dataclasses import dataclass

@dataclass
class AnalysisStatistics:
    """
    Mutable statistics tracking analysis extraction metrics.
    Passed by reference into the AnalysisContext.
    """
    analyzed_modules: int = 0
    discovered_artifacts: int = 0
    extracted_operations: int = 0
    dependency_count: int = 0
    constraint_count: int = 0
    verification_count: int = 0
    rollback_count: int = 0
