"""Streaming statistics aggregation for the Coding Dataset."""

from collections import defaultdict
from typing import Any
from generators.common.statistics.base_statistics import BaseStatistics
from generators.coding.validation.schema import CodingDatasetRecord


class CodingStatistics(BaseStatistics):  # type: ignore[misc]
    """Aggregates generation metrics without holding the dataset in memory."""

    def __init__(self) -> None:
        super().__init__()
        self.artifact_type_distribution = defaultdict(int)  # type: ignore[var-annotated]
        self.operation_type_distribution = defaultdict(int)  # type: ignore[var-annotated]

        self.total_artifacts = 0
        self.total_operations = 0
        self.total_dependencies = 0
        self.total_context_size = 0

    def add_sample(self, record: CodingDatasetRecord, json_str: str) -> None:
        self._add_base_sample(record, json_str)

        # Track context size (number of keys/lists)
        if record.context:
            self.total_context_size += len(record.context.get("existing_models", [])) + len(
                record.context.get("existing_views", [])
            )

        if hasattr(record.output, "artifacts"):
            artifacts = record.output.artifacts
            self.total_artifacts += len(artifacts)
            for a in artifacts:
                self.artifact_type_distribution[a.language] += 1
                self.total_dependencies += len(getattr(a, "dependencies", []))

        if hasattr(record.output, "operations"):
            ops = record.output.operations
            self.total_operations += len(ops)
            for o in ops:
                self.operation_type_distribution[o.operation] += 1

    def get_manifest_data(self) -> dict[str, Any]:
        return {
            "average_artifact_count": round(self.total_artifacts / max(1, self.total_samples), 2),
            "average_operation_count": round(self.total_operations / max(1, self.total_samples), 2),
        }

    def get_export_stats(self) -> dict[str, Any]:
        return {
            "artifact_type_distribution": dict(self.artifact_type_distribution),
            "operation_type_distribution": dict(self.operation_type_distribution),
            "average_artifacts_per_sample": round(
                self.total_artifacts / max(1, self.total_samples), 2
            ),
            "average_operations_per_sample": round(
                self.total_operations / max(1, self.total_samples), 2
            ),
            "average_dependencies_per_artifact": round(
                self.total_dependencies / max(1, self.total_artifacts), 2
            ),
            "average_context_size": round(self.total_context_size / max(1, self.total_samples), 2),
        }
