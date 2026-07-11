"""Static analysis engine to detect deterministic repair scenarios in Odoo modules."""

import ast
import logging
from pathlib import Path

from preprocessing.domain.repository import PreprocessedModule
from preprocessing.domain.file import NormalizedFile, Language
from generators.repair.validation.schema import ArtifactType

from generators.repair.analysis.rules.base import AnalyzeContext, RepairOpportunity
from generators.repair.analysis.rules.missing_sudo import MissingSudoRule
from generators.repair.analysis.rules.api_multi import ApiMultiRule
from generators.repair.analysis.rules.deprecated_attrs import DeprecatedAttrsRule

logger = logging.getLogger(__name__)


class RepairAnalyzer:
    """Analyzes Odoo source code for known anti-patterns and generates repair opportunities."""

    def __init__(self) -> None:
        self.rules = [MissingSudoRule(), ApiMultiRule(), DeprecatedAttrsRule()]

    def analyze(self, module: PreprocessedModule) -> list[RepairOpportunity]:
        opportunities = []
        base_path = Path(str(module.metadata["path"]))
        for file in module.files:
            if file.language == Language.PYTHON:
                opportunities.extend(self._analyze_python(file, base_path, module.name))
            elif file.language == Language.XML:
                opportunities.extend(self._analyze_xml(file, base_path, module.name))

        return opportunities

    def _analyze_python(
        self, file: NormalizedFile, base_path: Path, module_name: str
    ) -> list[RepairOpportunity]:
        opportunities = []  # type: ignore[var-annotated]
        try:
            content = file.normalized_content
            lines = content.splitlines()
            tree = ast.parse(content, filename=str(file.normalized_path))
        except Exception:
            logger.exception("Failed to parse %s", file.normalized_path)
            return opportunities

        context = AnalyzeContext(
            module_name=module_name,
            file_path=file.normalized_path,
            base_path=base_path,
            content=content,
            lines=lines,
            tree=tree,
        )

        for rule in self.rules:
            if ArtifactType.PYTHON in rule.target_artifacts:
                try:
                    opportunities.extend(rule.detect(context))
                except Exception:
                    logger.exception(
                        "Repair Rule Failed\n\nModule:\n%s\n\nFile:\n%s\n\nRule:\n%s\n\nRule Name:\n%s\n\nException:",
                        context.module_name,
                        context.file_path,
                        rule.rule_id,
                        rule.title,
                    )

        return opportunities

    def _analyze_xml(
        self, file: NormalizedFile, base_path: Path, module_name: str
    ) -> list[RepairOpportunity]:
        opportunities = []  # type: ignore[var-annotated]
        try:
            content = file.normalized_content
            lines = content.splitlines()
        except Exception:
            logger.exception("Failed to parse %s", file.normalized_path)
            return opportunities

        context = AnalyzeContext(
            module_name=module_name,
            file_path=file.normalized_path,
            base_path=base_path,
            content=content,
            lines=lines,
            tree=None,
        )

        for rule in self.rules:
            if ArtifactType.XML in rule.target_artifacts:
                try:
                    opportunities.extend(rule.detect(context))
                except Exception:
                    logger.exception(
                        "Repair Rule Failed\n\nModule:\n%s\n\nFile:\n%s\n\nRule:\n%s\n\nRule Name:\n%s\n\nException:",
                        context.module_name,
                        context.file_path,
                        rule.rule_id,
                        rule.title,
                    )

        return opportunities
