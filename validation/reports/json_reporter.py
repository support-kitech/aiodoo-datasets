"""JSON reporter for machine-readable output."""

import json
import dataclasses
from enum import Enum
from pathlib import Path
from types import MappingProxyType

from validation.domain.results import ValidationReport
from validation.reports.base import BaseReporter


class _ReportEncoder(json.JSONEncoder):
    """Encodes frozen dataclasses, MappingProxies, Enums, and Paths."""

    def default(self, obj):
        if dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, MappingProxyType):
            return dict(obj)
        if isinstance(obj, Path):
            return str(obj)
        return super().default(obj)


class JsonReporter(BaseReporter):
    """Writes a deterministic JSON validation report."""

    def report(self, report: ValidationReport, output_dir: Path) -> None:
        """Write validation_report.json to output_dir."""
        report_path = output_dir / "validation_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, cls=_ReportEncoder, indent=2, sort_keys=True, ensure_ascii=False)
