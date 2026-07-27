"""Builds the default RuleRegistry with all shared and generator-specific rules."""

from validation.rules.registry import RuleRegistry

# Schema rules
from validation.rules.schema.required_fields import RequiredFieldsRule
from validation.rules.schema.field_types import FieldTypeRule
from validation.rules.schema.record_structure import RecordStructureRule

# Metadata rules
from validation.rules.metadata.required_metadata import RequiredMetadataRule
from validation.rules.metadata.version_format import VersionFormatRule
from validation.rules.metadata.timestamp_format import TimestampFormatRule

# Integrity rules
from validation.rules.integrity.hash_verification import HashVerificationRule
from validation.rules.integrity.duplicate_detection import DuplicateDetectionRule
from validation.rules.integrity.deterministic_id import DeterministicIdRule

# Reference rules
from validation.rules.references.orphan_detection import OrphanReferenceRule
from validation.rules.references.circular_refs import CircularReferenceRule

# Serialization rules
from validation.rules.serialization.encoding import EncodingRule

# Generator-specific rules
from validation.rules.generators.planner import PlannerTasksNonEmptyRule, PlannerGoalNonEmptyRule
from validation.rules.generators.coding import (
    CodingArtifactsNonEmptyRule,
    CodingArtifactValidPathRule,
)
from validation.rules.generators.repair import RepairTaskStructureRule, RepairOperationsRule
from validation.rules.generators.context import ContextQueryRule
from validation.rules.generators.execution import ExecutionInstructionRule
from validation.rules.generators.approval import (
    ApprovalBoundedEvidenceRule,
    ApprovalDecisionRule,
    ApprovalIdentityRule,
    ApprovalProductionScaleRule,
)
from validation.rules.generators.conversation import (
    ConversationBoundedHistoryRule,
    ConversationIdentityRule,
    ConversationInstructionRule,
    ConversationProductionScaleRule,
)
from validation.rules.generators.evaluation import (
    EvaluationCatalogRule,
    EvaluationIdentityRule,
    EvaluationProductionScaleRule,
)
from validation.rules.generators.eval_corpus import EvalCorpusContractRule
from validation.rules.generators.contract_compliance import build_contract_compliance_rules


class RuleBuilder:
    """Constructs the default RuleRegistry with all rules registered and frozen."""

    @staticmethod
    def build_default() -> RuleRegistry:
        """Create a registry with all production rules, frozen and ready."""
        registry = RuleRegistry()

        # Schema
        registry.register_many(
            RequiredFieldsRule(),
            FieldTypeRule(),
            RecordStructureRule(),
        )

        # Metadata
        registry.register_many(
            RequiredMetadataRule(),
            VersionFormatRule(),
            TimestampFormatRule(),
        )

        # Integrity
        registry.register_many(
            HashVerificationRule(),
            DuplicateDetectionRule(),
            DeterministicIdRule(),
        )

        # References
        registry.register_many(
            OrphanReferenceRule(),
            CircularReferenceRule(),
        )

        # Serialization
        registry.register_many(
            EncodingRule(),
        )

        # Generator-specific
        registry.register_many(
            PlannerTasksNonEmptyRule(),
            PlannerGoalNonEmptyRule(),
            CodingArtifactsNonEmptyRule(),
            CodingArtifactValidPathRule(),
            RepairTaskStructureRule(),
            RepairOperationsRule(),
            ContextQueryRule(),
            ExecutionInstructionRule(),
            ApprovalDecisionRule(),
            ApprovalIdentityRule(),
            ApprovalBoundedEvidenceRule(),
            ApprovalProductionScaleRule(),
            ConversationInstructionRule(),
            ConversationIdentityRule(),
            ConversationBoundedHistoryRule(),
            ConversationProductionScaleRule(),
            EvaluationCatalogRule(),
            EvaluationIdentityRule(),
            EvaluationProductionScaleRule(),
            EvalCorpusContractRule(),
        )

        # Contract compliance (aiodoo_contract) — one rule per capability.
        registry.register_many(*build_contract_compliance_rules())

        registry.freeze()
        return registry
