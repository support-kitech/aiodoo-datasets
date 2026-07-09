"""Streaming statistics aggregation for the Planner Dataset."""

from typing import Any
from aiodoo_datasets.generators.common.statistics.base_statistics import BaseStatistics
from aiodoo_datasets.generators.planner.validation.schema import PlannerDatasetRecord

class PlannerStatistics(BaseStatistics):
    """Aggregates generation metrics without holding the dataset in memory."""
    def __init__(self):
        super().__init__()
        self.total_tasks = 0
        self.total_dependencies = 0
        
    def add_sample(self, record: PlannerDatasetRecord, json_str: str) -> None:
        self._add_base_sample(record, json_str)
        
        # Count tasks and dependencies safely from the Pydantic model
        if hasattr(record.output, "tasks"):
            tasks = record.output.tasks
            self.total_tasks += len(tasks)
            for t in tasks:
                self.total_dependencies += len(getattr(t, "dependencies", []))

    def get_manifest_data(self) -> dict[str, Any]:
        return {
            "average_task_count": round(self.total_tasks / max(1, self.total_samples), 2),
            "average_dependency_count": round(self.total_dependencies / max(1, self.total_tasks), 2)
        }

    def get_export_stats(self) -> dict[str, Any]:
        return {
            "average_tasks_per_sample": round(self.total_tasks / max(1, self.total_samples), 2),
            "average_dependencies_per_task": round(self.total_dependencies / max(1, self.total_tasks), 2)
        }
