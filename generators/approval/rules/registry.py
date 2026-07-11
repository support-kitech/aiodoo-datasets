"""Rule registry for the Approval Generator."""

from typing import Dict, List, Type, TYPE_CHECKING
from aiodoo_datasets.generators.approval.rules.base_rule import BaseRule
from aiodoo_datasets.generators.approval.exceptions import ValidationException
from aiodoo_datasets.generators.approval.enums import RuleCategory

if TYPE_CHECKING:
    from aiodoo_datasets.generators.approval.rules.rule_set import RuleSet


class RuleRegistry:
    """Deterministic registry for approval rules."""

    _rules: Dict[str, Type[BaseRule]] = {}
    _priorities: Dict[int, str] = {}

    @classmethod
    def register(cls, rule_class: Type[BaseRule]) -> None:
        """Register a rule and validate metadata."""
        # Validation
        if not hasattr(rule_class, "RULE_ID") or not rule_class.RULE_ID:
            raise ValidationException(f"Rule {rule_class.__name__} missing RULE_ID")
        if not hasattr(rule_class, "PRIORITY"):
            raise ValidationException(f"Rule {rule_class.__name__} missing PRIORITY")
        if not hasattr(rule_class, "RULE_CATEGORY") or not isinstance(
            rule_class.RULE_CATEGORY, RuleCategory
        ):
            raise ValidationException(f"Rule {rule_class.__name__} has invalid RULE_CATEGORY")

        rule_id = rule_class.RULE_ID
        priority = rule_class.PRIORITY

        if rule_id in cls._rules:
            raise ValidationException(f"Duplicate RULE_ID found: {rule_id}")
        if priority in cls._priorities:
            raise ValidationException(
                f"Duplicate priority {priority} for rules {cls._priorities[priority]} and {rule_id}"
            )

        cls._rules[rule_id] = rule_class
        cls._priorities[priority] = rule_id

    @classmethod
    def get_all_rules(cls) -> List[BaseRule]:
        """Get instances of all registered rules, sorted by priority."""
        sorted_priorities = sorted(cls._priorities.keys())
        return [cls._rules[cls._priorities[p]]() for p in sorted_priorities]

    @classmethod
    def clear(cls) -> None:
        """Clear the registry (useful for tests)."""
        cls._rules.clear()
        cls._priorities.clear()

    @classmethod
    def compile(cls) -> "RuleSet":
        """Compile the registry into an immutable RuleSet."""
        from aiodoo_datasets.generators.approval.rules.rule_set import RuleSet

        rules = cls.get_all_rules()
        return RuleSet(rules=tuple(rules))
