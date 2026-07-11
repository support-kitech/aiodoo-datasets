"""Rule to detect deprecated attrs in XML views."""

import hashlib
from generators.repair.analysis.rules.base import (
    BaseRepairRule,
    AnalyzeContext,
    RepairOpportunity,
)
from generators.repair.validation.schema import RepairSeverity, ArtifactType


class DeprecatedAttrsRule(BaseRepairRule):  # type: ignore[misc]
    rule_id = "RP003"
    title = "Deprecated attrs"
    description = "Detects deprecated 'attrs' attributes in XML views."
    severity = RepairSeverity.MEDIUM
    category = "Migration"
    supported_versions = "17+"
    target_artifacts = [ArtifactType.XML]

    def detect(self, context: AnalyzeContext) -> list[RepairOpportunity]:
        opportunities = []
        for i, line in enumerate(context.lines):
            if 'attrs="' in line:
                line_num = i + 1
                rel_path = str(context.file_path.relative_to(context.base_path))
                deterministic_id = hashlib.sha256(
                    f"{context.module_name}:{rel_path}:{line_num}:{self.rule_id}".encode()
                ).hexdigest()

                opportunities.append(
                    RepairOpportunity(
                        id=deterministic_id,
                        artifact_path=rel_path,
                        artifact_type=ArtifactType.XML,
                        problem_description="Deprecated 'attrs' attribute used in view.",
                        severity=self.severity,
                        root_cause="Odoo 17+ replaces attrs with invisible=, readonly=, etc.",
                        location=f"Line {line_num}",
                        code_snippet=line.strip(),
                        operations=[
                            {"operation": "replace", "search": 'attrs="', "replace": 'invisible="'}
                        ],
                        explanation="The attrs attribute is fully deprecated in recent Odoo versions.",
                        rule_id=self.rule_id,
                        rule_title=self.title,
                        category=self.category,
                        supported_versions=self.supported_versions,
                        detector_name=self.__class__.__name__,
                        line_num=line_num,
                    )
                )
        return opportunities
