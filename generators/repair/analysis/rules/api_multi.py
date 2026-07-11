"""Rule to detect deprecated @api.multi decorators."""

import ast
import hashlib
from aiodoo_datasets.generators.repair.analysis.rules.base import (
    BaseRepairRule,
    AnalyzeContext,
    RepairOpportunity,
)
from aiodoo_datasets.generators.repair.validation.schema import RepairSeverity, ArtifactType


class ApiMultiRule(BaseRepairRule):
    rule_id = "RP002"
    title = "Deprecated api.multi"
    description = "Detects deprecated @api.multi decorators in Python files."
    severity = RepairSeverity.LOW
    category = "Migration"
    supported_versions = "8-12"
    target_artifacts = [ArtifactType.PYTHON]

    def detect(self, context: AnalyzeContext) -> list[RepairOpportunity]:
        opportunities = []
        if not context.tree:
            return opportunities

        for node in ast.walk(context.tree):
            if isinstance(node, ast.FunctionDef):
                for decorator in node.decorator_list:
                    if (
                        isinstance(decorator, ast.Attribute)
                        and getattr(decorator.value, "id", "") == "api"
                        and decorator.attr == "multi"
                    ):
                        line_num = decorator.lineno
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
                                problem_description="Deprecated @api.multi decorator used.",
                                severity=self.severity,
                                root_cause="Odoo 13+ removes the need for @api.multi.",
                                location=f"Line {line_num}",
                                code_snippet=snippet,
                                operations=[
                                    {"operation": "replace", "search": snippet, "replace": ""}
                                ],
                                explanation="@api.multi is deprecated and no longer needed in modern Odoo.",
                                rule_id=self.rule_id,
                                rule_title=self.title,
                                category=self.category,
                                supported_versions=self.supported_versions,
                                detector_name=self.__class__.__name__,
                                line_num=line_num,
                            )
                        )
        return opportunities
