"""Base classes for modular repair rules."""

import ast
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

from aiodoo_datasets.generators.repair.validation.schema import RepairSeverity, ArtifactType

@dataclass
class RepairOpportunity:
    id: str
    artifact_path: str
    artifact_type: ArtifactType
    problem_description: str
    severity: RepairSeverity
    root_cause: str
    location: str
    code_snippet: str
    operations: list[dict]
    explanation: str
    rule_id: str
    rule_title: str
    category: str
    supported_versions: str
    detector_name: str
    line_num: int

@dataclass
class AnalyzeContext:
    module_name: str
    file_path: Path
    base_path: Path
    content: str
    lines: list[str]
    tree: Optional[ast.AST] = None

class BaseRepairRule:
    """Base interface for all static analysis repair rules."""
    
    rule_id: str = "UNKNOWN"
    title: str = "Unknown Rule"
    description: str = ""
    severity: RepairSeverity = RepairSeverity.LOW
    category: str = "Uncategorized"
    supported_versions: str = "8+"
    target_artifacts: list[ArtifactType] = []

    def detect(self, context: AnalyzeContext) -> list[RepairOpportunity]:
        """Detect issues in the provided context and return opportunities."""
        raise NotImplementedError("Rules must implement detect()")
