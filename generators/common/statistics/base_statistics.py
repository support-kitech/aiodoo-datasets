"""Base statistics aggregation for AIODOO Dataset Generators."""

import json
from pathlib import Path
from collections import defaultdict
from typing import Any


class BaseStatistics:
    """Aggregates base generation metrics shared across all pipelines."""

    def __init__(self) -> None:
        self.total_modules: int = 0
        self._seen_modules: set[str] = set()
        self.total_samples: int = 0

        self.version_distribution: defaultdict[str, int] = defaultdict(int)
        self.edition_distribution: defaultdict[str, int] = defaultdict(int)
        self.scenario_distribution: defaultdict[str, int] = defaultdict(int)
        self.difficulty_distribution: defaultdict[int, int] = defaultdict(int)

        self.duplicate_count = 0
        self.validation_failures = 0
        self.total_tokens = 0

    def record_duplicate(self) -> None:
        self.duplicate_count += 1

    def record_validation_failure(self) -> None:
        self.validation_failures += 1

    def _add_base_sample(self, record: Any, json_str: str) -> None:
        self.total_samples += 1

        metadata = record.metadata
        if isinstance(metadata, dict):
            module_name = metadata.get("module", "unknown")
            version = metadata.get("odoo_version") or metadata.get("version", "unknown")
            edition = metadata.get("edition", "unknown")
            scenario = metadata.get("scenario", [])
            difficulty = metadata.get("difficulty", 1)
        else:
            module_name = getattr(metadata, "module", getattr(metadata, "source_module", "unknown"))
            version = getattr(metadata, "odoo_version", getattr(metadata, "version", "unknown"))
            edition = getattr(metadata, "edition", "unknown")
            scenario = getattr(metadata, "scenario", [])
            difficulty = getattr(metadata, "difficulty", 1)

        if module_name not in self._seen_modules:
            self._seen_modules.add(module_name)
            self.total_modules = len(self._seen_modules)

        self.version_distribution[version] += 1
        self.edition_distribution[edition] += 1

        if scenario:
            # Handle scenario string vs list gracefully
            scenario_val = scenario[0] if isinstance(scenario, list) else scenario
            self.scenario_distribution[scenario_val] += 1

        self.difficulty_distribution[difficulty] += 1

        self.total_tokens += len(json_str) // 4

    def get_manifest_data(self) -> dict[str, Any]:
        """Override in subclasses to provide specific manifest metrics."""
        return {}

    def get_export_stats(self) -> dict[str, Any]:
        """Override in subclasses to provide specific export metrics."""
        return {}

    def export(self, output_path: Path) -> None:
        """Dump the aggregated statistics to a JSON file."""
        stats = {
            "total_modules": self.total_modules,
            "total_samples": self.total_samples,
            "version_distribution": dict(self.version_distribution),
            "edition_distribution": dict(self.edition_distribution),
            "scenario_distribution": dict(self.scenario_distribution),
            "difficulty_distribution": dict(self.difficulty_distribution),
            "duplicate_count": self.duplicate_count,
            "validation_failures": self.validation_failures,
            "average_token_estimate": round(self.total_tokens / max(1, self.total_samples), 2),
        }
        stats.update(self.get_export_stats())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4)
