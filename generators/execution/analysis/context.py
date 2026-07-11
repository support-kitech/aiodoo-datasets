"""Analysis Context definition."""

from dataclasses import dataclass, field
from typing import Any
from generators.common.discovery.scanner import OdooModule
from generators.common.discovery.ast_parser import PythonKnowledge
from generators.common.discovery.xml_parser import XMLKnowledge
from generators.execution.statistics.analysis_statistics import AnalysisStatistics


@dataclass(frozen=True, eq=True)
class AnalysisContext:
    """
    Immutable shared state passed to all analyzers during the discovery phase.

    Attributes:
        module: The Odoo module being analyzed.
        python_knowledge: Discovered Python AST knowledge.
        xml_knowledge: Discovered XML knowledge.
        csv_knowledge: Discovered CSV knowledge.
        shared_results: Any pre-computed analysis from other generators (e.g., Planner).
        config: Environment configuration dictionary.
        statistics: Mutable statistics collector (reference is frozen, but internal state mutates).
    """

    module: OdooModule
    python_knowledge: PythonKnowledge
    xml_knowledge: XMLKnowledge
    csv_knowledge: dict[str, Any] = field(default_factory=dict)
    shared_results: dict[str, Any] = field(default_factory=dict)
    config: dict[str, Any] = field(default_factory=dict)
    statistics: AnalysisStatistics = field(default_factory=AnalysisStatistics)
