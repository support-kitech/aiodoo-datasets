"""Context Generator specific statistics tracking."""

from collections import defaultdict
from typing import Any

from generators.common.statistics.base_statistics import BaseStatistics
from generators.context.protocol.schema import ContextTask


class ContextStatistics(BaseStatistics):  # type: ignore[misc]
    """Aggregates context generation metrics."""

    def __init__(self) -> None:
        super().__init__()
        self.nodes_discovered = 0
        self.edges_discovered = 0
        self.queries_generated = 0
        self.ranking_results = 0
        self.relationships_extracted = 0

        self.query_type_counts = defaultdict(int)  # type: ignore[var-annotated]
        self.ranking_rule_counts = defaultdict(int)  # type: ignore[var-annotated]

    def add_sample(self, record: ContextTask, json_str: str) -> None:
        """Processes a single validated context protocol record."""

        class DummyRecord:
            def __init__(self, metadata) -> None:  # type: ignore[no-untyped-def]
                self.metadata = metadata

        dummy = DummyRecord(record.metadata.model_dump())
        self._add_base_sample(dummy, json_str)
        self.queries_generated += 1

        self.nodes_discovered += len(record.graph.nodes)
        self.edges_discovered += len(record.graph.edges)

        self.ranking_results += len(record.artifacts)
        self.relationships_extracted += len(record.graph.edges)

        self.query_type_counts[record.query.query_type.value] += 1

        for artifact in record.artifacts:
            self.ranking_rule_counts[artifact.ranking_reason.value] += 1

    def get_export_stats(self) -> dict[str, Any]:
        """Provides context-specific export metrics."""
        avg_artifacts = round(self.ranking_results / max(1, self.queries_generated), 2)
        avg_edges = round(self.relationships_extracted / max(1, self.queries_generated), 2)

        return {
            "nodes_discovered": self.nodes_discovered,
            "edges_discovered": self.edges_discovered,
            "queries_generated": self.queries_generated,
            "ranking_results": self.ranking_results,
            "relationships_extracted": self.relationships_extracted,
            "query_type_counts": dict(self.query_type_counts),
            "ranking_rule_counts": dict(self.ranking_rule_counts),
            "average_artifacts_per_query": avg_artifacts,
            "average_relationships_per_query": avg_edges,
        }
