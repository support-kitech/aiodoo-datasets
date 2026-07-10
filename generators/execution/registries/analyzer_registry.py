"""Static registry for all analysis plugins."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.artifact_analyzer import ArtifactAnalyzer
from aiodoo_datasets.generators.execution.analysis.operation_analyzer import OperationAnalyzer
from aiodoo_datasets.generators.execution.analysis.dependency_analyzer import DependencyAnalyzer
from aiodoo_datasets.generators.execution.analysis.constraint_analyzer import ConstraintAnalyzer
from aiodoo_datasets.generators.execution.analysis.verification_analyzer import VerificationAnalyzer
from aiodoo_datasets.generators.execution.analysis.rollback_analyzer import RollbackAnalyzer
from aiodoo_datasets.generators.execution.analysis.metadata_analyzer import MetadataAnalyzer

# Statically registered analyzers in execution order
_REGISTERED_ANALYZERS: tuple[type[BaseAnalyzer], ...] = (
    ArtifactAnalyzer,
    OperationAnalyzer,
    DependencyAnalyzer,
    ConstraintAnalyzer,
    VerificationAnalyzer,
    RollbackAnalyzer,
    MetadataAnalyzer,
)

class AnalyzerRegistry:
    """Manages the deterministic loading of analysis plugins."""
    
    @classmethod
    def get_analyzers(cls) -> tuple[BaseAnalyzer, ...]:
        """Returns instantiated analyzers sorted explicitly by priority."""
        instances = [analyzer_cls() for analyzer_cls in _REGISTERED_ANALYZERS]
        
        # Validate unique priorities
        priorities = set()
        for inst in instances:
            if not hasattr(inst, "PRIORITY"):
                raise ValueError(f"{inst.__class__.__name__} missing PRIORITY")
            if inst.PRIORITY in priorities:
                raise ValueError(f"Duplicate PRIORITY {inst.PRIORITY} found in {inst.__class__.__name__}")
            priorities.add(inst.PRIORITY)
            
        return tuple(sorted(instances, key=lambda a: a.PRIORITY))
