"""Rule to detect missing sudo() with cr.execute."""

import ast
import hashlib
from generators.repair.analysis.rules.base import (
    BaseRepairRule,
    AnalyzeContext,
    RepairOpportunity,
)
from generators.repair.validation.schema import RepairSeverity, ArtifactType


class MissingSudoRule(BaseRepairRule):  # type: ignore[misc]
    rule_id = "RP001"
    title = "Missing sudo()"
    description = (
        "Detects cr.execute() calls that bypass ORM security rules without explicit sudo()."
    )
    severity = RepairSeverity.HIGH
    category = "Security"
    supported_versions = "8+"
    target_artifacts = [ArtifactType.PYTHON]

    def detect(self, context: AnalyzeContext) -> list[RepairOpportunity]:
        opportunities = []  # type: ignore[var-annotated]
        if not context.tree:
            return opportunities

        for node in ast.walk(context.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr == "execute" and isinstance(node.func.value, ast.Attribute):
                    if node.func.value.attr == "cr":
                        line_num = node.lineno
                        snippet = context.lines[line_num - 1].strip()
                        rel_path = str(context.file_path.relative_to(context.base_path))

                        deterministic_id = hashlib.sha256(
                            f"{context.module_name}:{rel_path}:{line_num}:{self.rule_id}".encode()
                        ).hexdigest()

                        opportunities.append(
                            RepairOpportunity(
                                id=deterministic_id,
                                artifact_path=rel_path,
                                artifact_type=ArtifactType.PYTHON,
                                problem_description="Direct SQL execution without sudo bypasses record rules.",
                                severity=self.severity,
                                root_cause="Security vulnerability: cr.execute used directly.",
                                location=f"Line {line_num}",
                                code_snippet=snippet,
                                operations=[
                                    {
                                        "operation": "replace",
                                        "search": snippet,
                                        "replace": snippet.replace(
                                            "cr.execute", "sudo().cr.execute"
                                        ),
                                    }
                                ],
                                explanation="Direct SQL execution skips ORM security rules. Ensure it is intentional or use sudo().",
                                rule_id=self.rule_id,
                                rule_title=self.title,
                                category=self.category,
                                supported_versions=self.supported_versions,
                                detector_name=self.__class__.__name__,
                                line_num=line_num,
                            )
                        )
        return opportunities
