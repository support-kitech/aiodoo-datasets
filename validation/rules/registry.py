"""Freezable rule registry for the Validation Framework."""

import hashlib
from typing import Mapping
from types import MappingProxyType

from validation.domain.enums import ValidationCategory
from validation.exceptions import ValidationError
from validation.rules.base import BaseRule


class RuleRegistry:
    """
    A freezable registry of validation rules.

    Lifecycle: Create → Register → Freeze → Lookup Only

    After freeze(), rules are sorted by priority then rule_id for
    deterministic execution. Any mutation attempt raises ValidationError.
    """

    def __init__(self) -> None:
        self._rules: list[BaseRule] = []
        self._rule_ids: set[str] = set()
        self._frozen: bool = False

    def _assert_mutable(self) -> None:
        """Raise if the registry has been frozen."""
        if self._frozen:
            raise ValidationError("Cannot mutate a frozen RuleRegistry.")

    def register(self, rule: BaseRule) -> None:
        """Register a single rule. Raises on duplicate rule_id."""
        self._assert_mutable()
        if rule.rule_id in self._rule_ids:
            raise ValidationError(f"Duplicate rule registration: {rule.rule_id}")
        self._rules.append(rule)
        self._rule_ids.add(rule.rule_id)

    def register_many(self, *rules: BaseRule) -> None:
        """Register multiple rules at once."""
        for rule in rules:
            self.register(rule)

    def freeze(self) -> None:
        """Lock the registry and sort rules deterministically."""
        self._assert_mutable()
        self._rules.sort(key=lambda r: (r.priority, r.rule_id))
        self._frozen = True

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    def get_rules_for_dataset(self, dataset_name: str) -> tuple[BaseRule, ...]:
        """Return all applicable rules for a dataset, in priority order."""
        generator = self._infer_generator(dataset_name)
        return tuple(
            r
            for r in self._rules
            if r.enabled and (not r.target_generators or generator in r.target_generators)
        )

    def get_rules_by_category(self, category: ValidationCategory) -> tuple[BaseRule, ...]:
        """Return all enabled rules in a specific category."""
        return tuple(r for r in self._rules if r.enabled and r.category == category)

    @property
    def all_rules(self) -> tuple[BaseRule, ...]:
        """Return all registered rules in priority order."""
        return tuple(self._rules)

    @property
    def hash_value(self) -> str:
        """Deterministic SHA-256 hash of all registered rule IDs."""
        sha256 = hashlib.sha256()
        for rule in self._rules:
            sha256.update(f"{rule.rule_id}:{rule.severity.value}".encode("utf-8"))
            sha256.update(b"\x00")
        return sha256.hexdigest()

    @staticmethod
    def _infer_generator(dataset_name: str) -> str:
        """Infer the generator name from the dataset filename."""
        name = dataset_name.lower()
        for gen in (
            "planner",
            "coding",
            "repair",
            "context",
            "execution",
            "approval",
            "conversation",
            "evaluation",
        ):
            if gen in name:
                return gen
        return "unknown"

    @property
    def rules(self) -> Mapping[str, BaseRule]:
        """Return a read-only mapping of rule_id → rule."""
        return MappingProxyType({r.rule_id: r for r in self._rules})
