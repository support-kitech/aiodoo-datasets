"""Base class for all approval rules."""

from abc import ABC, abstractmethod
from typing import ClassVar
from generators.approval.rules.rule_context import RuleContext
from generators.approval.rules.rule_result import RuleResult
from generators.approval.enums import RuleCategory, Severity


class BaseRule(ABC):
    """Abstract base class for an approval rule plugin."""

    RULE_ID: ClassVar[str]
    RULE_NAME: ClassVar[str]
    RULE_CATEGORY: ClassVar[RuleCategory]
    SEVERITY: ClassVar[Severity]
    DESCRIPTION: ClassVar[str]
    VERSION: ClassVar[str]
    PRIORITY: ClassVar[int]

    @abstractmethod
    def evaluate(self, context: RuleContext) -> RuleResult:
        """Evaluate the rule against the provided context."""
        pass
