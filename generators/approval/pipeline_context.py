"""Pipeline context for the Approval Generator."""

from dataclasses import dataclass
from typing import Mapping, Any
from generators.approval.config.approval_config import ApprovalConfig
from generators.approval.domain.metadata import ReviewMetadata
from generators.approval.rules.rule_set import RuleSet
from generators.approval.rules.registry import RuleRegistry
from generators.approval.analysis.parsers.parser_registry import ParserRegistry


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """State context orchestrating the entire approval pipeline."""

    config: ApprovalConfig
    input_protocols: Mapping[str, Mapping[str, Any]]
    metadata: ReviewMetadata
    rule_set: RuleSet
    parser_registry_cls: type[ParserRegistry] = ParserRegistry
    rule_registry_cls: type[RuleRegistry] = RuleRegistry
