"""Repair-specific metrics accumulation subclass."""

from collections import defaultdict
from aiodoo_datasets.generators.common.statistics.base_statistics import BaseStatistics
from aiodoo_datasets.generators.repair.validation.schema import RepairDatasetRecord
from typing import Any


class RepairStatistics(BaseStatistics):
    """Tracks metrics specific to the Repair dataset generation process."""

    def __init__(self):
        super().__init__()
        self.total_opportunities_found = 0
        self.total_operations = 0

        self.severity_counts = defaultdict(int)
        self.rule_frequency = defaultdict(int)
        self.category_frequency = defaultdict(int)
        self.artifact_type_frequency = defaultdict(int)
        self.version_frequency = defaultdict(int)
        self.module_frequency = defaultdict(int)

    def add_sample(self, record: RepairDatasetRecord, json_str: str) -> None:
        self._add_base_sample(record, json_str)

        version = record.metadata.get("version", "unknown")
        module_name = record.metadata.get("module", "unknown")
        self.version_frequency[version] += 1
        self.module_frequency[module_name] += 1

        if hasattr(record.output, "tasks"):
            for task in record.output.tasks:
                self.total_opportunities_found += 1

                # Severity
                severity = (
                    task.problem.severity.lower() if hasattr(task.problem, "severity") else "low"
                )
                self.severity_counts[severity] += 1

                # Rule & Category metadata
                if hasattr(task, "metadata") and task.metadata:
                    rule_id = task.metadata.get("rule_id", "unknown")
                    category = task.metadata.get("category", "unknown")
                    self.rule_frequency[rule_id] += 1
                    self.category_frequency[category] += 1

                # Artifact Type
                if hasattr(task, "artifacts"):
                    for artifact in task.artifacts:
                        art_type = artifact.type if hasattr(artifact, "type") else "unknown"
                        if hasattr(art_type, "value"):
                            art_type = art_type.value
                        self.artifact_type_frequency[art_type] += 1

                # Operations
                if hasattr(task, "expected_outcome") and hasattr(
                    task.expected_outcome, "operations"
                ):
                    self.total_operations += len(task.expected_outcome.operations)

    def get_manifest_data(self) -> dict[str, Any]:
        return {
            "average_tasks_per_sample": round(
                self.total_opportunities_found / max(1, self.total_samples), 2
            ),
            "average_operations_per_task": round(
                self.total_operations / max(1, self.total_opportunities_found), 2
            ),
        }

    def get_export_stats(self) -> dict[str, Any]:
        return {
            "total_opportunities_found": self.total_opportunities_found,
            "total_operations": self.total_operations,
            "severity_distribution": dict(self.severity_counts),
            "rule_frequency": dict(self.rule_frequency),
            "category_frequency": dict(self.category_frequency),
            "artifact_type_frequency": dict(self.artifact_type_frequency),
            "version_frequency": dict(self.version_frequency),
            "module_frequency": dict(self.module_frequency),
        }
