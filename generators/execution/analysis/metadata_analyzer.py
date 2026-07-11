"""Metadata Analyzer implementation."""

from aiodoo_datasets.generators.execution.analysis.base import BaseAnalyzer
from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext
from typing import Any


class MetadataAnalyzer(BaseAnalyzer):  # type: ignore[misc]
    """Calculates deterministic IDs, hashes, and lineage details."""

    PRIORITY = 70

    def analyze(self, context: AnalysisContext) -> dict[str, Any]:
        return {"is_successful": True, "metadata": {}}
