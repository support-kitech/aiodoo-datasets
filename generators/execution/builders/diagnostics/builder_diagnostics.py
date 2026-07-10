from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.builders.diagnostics.warning import Warning
from aiodoo_datasets.generators.execution.builders.diagnostics.error import Error
from aiodoo_datasets.generators.execution.builders.diagnostics.skipped_item import SkippedItem

@dataclass(frozen=True, slots=True)
class BuilderDiagnostics:
    """
    A structured, immutable diagnostic container tracking execution anomalies.
    Replaces console logging with a queryable, serialization-friendly object.
    """
    warnings: tuple[Warning, ...] = field(default_factory=tuple)
    errors: tuple[Error, ...] = field(default_factory=tuple)
    skipped_items: tuple[SkippedItem, ...] = field(default_factory=tuple)
