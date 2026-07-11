"""Static analysis engine to detect deterministic repair scenarios in Odoo modules."""

import ast
import logging
from pathlib import Path

from aiodoo_datasets.generators.common.discovery.scanner import OdooModule
from aiodoo_datasets.generators.repair.validation.schema import ArtifactType

from aiodoo_datasets.generators.repair.analysis.rules.base import AnalyzeContext, RepairOpportunity
from aiodoo_datasets.generators.repair.analysis.rules.missing_sudo import MissingSudoRule
from aiodoo_datasets.generators.repair.analysis.rules.api_multi import ApiMultiRule
from aiodoo_datasets.generators.repair.analysis.rules.deprecated_attrs import DeprecatedAttrsRule

logger = logging.getLogger(__name__)


class RepairAnalyzer:
    """Analyzes Odoo source code for known anti-patterns and generates repair opportunities."""

    def __init__(self) -> None:
        self.rules = [MissingSudoRule(), ApiMultiRule(), DeprecatedAttrsRule()]

    def analyze(self, module: OdooModule) -> list[RepairOpportunity]:
        opportunities = []
        for py_file in module.path.rglob("*.py"):
            opportunities.extend(self._analyze_python(py_file, module.path, module.name))

        for xml_file in module.path.rglob("*.xml"):
            opportunities.extend(self._analyze_xml(xml_file, module.path, module.name))

        return opportunities

    def _analyze_python(
        self, py_file: Path, base_path: Path, module_name: str
    ) -> list[RepairOpportunity]:
        opportunities = []  # type: ignore[var-annotated]
        try:
            content = py_file.read_text(encoding="utf-8")
            lines = content.splitlines()
            tree = ast.parse(content, filename=str(py_file))
        except Exception:
            logger.exception("Failed to parse %s", py_file)
            return opportunities

        context = AnalyzeContext(
            module_name=module_name,
            file_path=py_file,
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
                        context.file_path.relative_to(context.base_path),
                        rule.rule_id,
                        rule.title,
                    )

        return opportunities

    def _analyze_xml(
        self, xml_file: Path, base_path: Path, module_name: str
    ) -> list[RepairOpportunity]:
        opportunities = []  # type: ignore[var-annotated]
        try:
            content = xml_file.read_text(encoding="utf-8")
            lines = content.splitlines()
        except Exception:
            logger.exception("Failed to parse %s", xml_file)
            return opportunities

        context = AnalyzeContext(
            module_name=module_name,
            file_path=xml_file,
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
                        context.file_path.relative_to(context.base_path),
                        rule.rule_id,
                        rule.title,
                    )

        return opportunities
