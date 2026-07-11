"""Decision engine for the Approval Generator."""

from aiodoo_datasets.generators.approval.engine.engine_context import EngineContext
from aiodoo_datasets.generators.approval.engine.engine_result import EngineResult
from aiodoo_datasets.generators.approval.engine.scoring import DecisionScorer
from aiodoo_datasets.generators.approval.engine.recommendation_builder import RecommendationBuilder
from aiodoo_datasets.generators.approval.engine.decision_builder import DecisionBuilder

from aiodoo_datasets.generators.approval.rules.rule_context import RuleContext
from aiodoo_datasets.generators.approval.rules.rule_set import RuleSet


class DecisionEngine:
    """Executes rules and aggregates the final review decision."""

    @staticmethod
    def execute(context: EngineContext, rule_set: RuleSet) -> EngineResult:
        """Run all registered rules against the collected evidence."""

        all_findings = []
        diagnostics = []
        rule_context = RuleContext(evidence_pool=context.evidence_pool, metadata=context.metadata)

        for rule in rule_set.rules:
            result = rule.evaluate(rule_context)
            all_findings.extend(result.findings)
            diagnostics.extend(result.diagnostics)

        findings_tuple = tuple(all_findings)

        decision_status, confidence, reasoning = DecisionScorer.evaluate_decision(findings_tuple)

        decision = DecisionBuilder.build(
            status=decision_status,
            confidence=confidence,
            reasoning=reasoning,
            findings=findings_tuple,
        )

        recommendations = RecommendationBuilder.build(findings_tuple)

        return EngineResult(
            success=True,
            decision=decision,
            findings=findings_tuple,
            recommendations=recommendations,
            diagnostics=tuple(diagnostics),
        )
