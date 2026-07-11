"""ReviewMetadata domain model."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class ReviewMetadata:
    """Traceability mapping back to the exact versions and protocols."""

    generator_version: str
    protocol_version: str
    schema_version: str
    source_module: str
    odoo_version: Optional[str] = None
    odoo_edition: Optional[str] = None
    planner_version: Optional[str] = None
    coding_version: Optional[str] = None
    execution_version: Optional[str] = None
    repair_version: Optional[str] = None
    complexity_score: Optional[int] = None
