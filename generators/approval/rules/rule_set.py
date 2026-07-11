"""Immutable set of compiled approval rules."""

from dataclasses import dataclass
from typing import Tuple
from aiodoo_datasets.generators.approval.rules.base_rule import BaseRule
from aiodoo_datasets.generators.approval.exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class RuleSet:
    """An immutable, deterministically ordered collection of validated rules."""

    rules: Tuple[BaseRule, ...]

    def __post_init__(self):
        """Ensure uniqueness of RULE_ID and strict ordering by PRIORITY."""
        rule_ids = set()
        last_priority = -1

        for rule in self.rules:
            if rule.RULE_ID in rule_ids:
                raise ValidationException(f"Duplicate RULE_ID in RuleSet: {rule.RULE_ID}")
            if rule.PRIORITY < last_priority:
                raise ValidationException("Rules in RuleSet are not strictly ordered by PRIORITY.")

            rule_ids.add(rule.RULE_ID)
            last_priority = rule.PRIORITY
