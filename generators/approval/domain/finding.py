"""Finding domain model."""

from dataclasses import dataclass, field
from typing import Tuple
from aiodoo_datasets.generators.approval.enums import Severity, RuleCategory
from aiodoo_datasets.generators.approval.domain.evidence import Evidence


@dataclass(frozen=True, slots=True)
class Finding:
    """A specific observation linked to Evidence. Can be positive or negative."""

    finding_id: str
    rule_id: str
    category: RuleCategory
    severity: Severity
    description: str
    evidence: Tuple[Evidence, ...] = field(default_factory=tuple)
    is_positive: bool = False
