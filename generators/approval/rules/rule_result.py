"""Result returned by a rule execution."""

from dataclasses import dataclass, field
from typing import Tuple, Mapping, Any
from generators.approval.domain.finding import Finding
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class RuleResult:
    """Result returned by a rule execution."""

    findings: Tuple[Finding, ...] = field(default_factory=tuple)
    diagnostics: Tuple[str, ...] = field(default_factory=tuple)
    statistics: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
