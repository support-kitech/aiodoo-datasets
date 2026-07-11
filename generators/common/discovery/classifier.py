"""Classifies extracted Odoo structural knowledge into rich engineering scenarios."""

from dataclasses import dataclass, field
from typing import Sequence

from .scanner import OdooModule
from .ast_parser import PythonKnowledge
from .xml_parser import XMLKnowledge


@dataclass(slots=True)
class Scenario:
    """Represents an identified engineering scenario."""

    name: str
    tags: list[str] = field(default_factory=list)
    difficulty: int = 1
    metrics: dict[str, int] = field(default_factory=dict)


class ScenarioClassifier:
    """Uses rich heuristics to classify structural code into training scenarios."""

    def classify(
        self,
        module: OdooModule,
        python_data: Sequence[PythonKnowledge],
        xml_data: Sequence[XMLKnowledge],
    ) -> list[Scenario]:
        scenarios = []

        has_transient = False
        has_controllers = False
        has_routes = False
        has_compute = False
        has_onchange = False

        has_views = False
        has_qweb = False
        has_reports = False
        has_security = False
        has_cron = False
        has_mail = False

        # Compute metrics
        metrics = {
            "models": 0,
            "fields": 0,
            "views": 0,
            "controllers": 0,
            "reports": 0,
            "security_rules": 0,
            "scheduled_actions": 0,
            "dependencies": len(module.manifest.depends),
            "assets": 0,
            "file_count": module.file_count,
        }

        for py_k in python_data:
            if py_k.routes:
                has_routes = True
            for model_name, model_def in py_k.models.items():
                if model_def.model_type == "models.TransientModel":
                    has_transient = True
                elif model_def.model_type == "http.Controller":
                    has_controllers = True
                    metrics["controllers"] += 1
                else:
                    metrics["models"] += 1

                metrics["fields"] += len(model_def.fields)

                for field_name, f_def in model_def.fields.items():
                    if f_def.computed:
                        has_compute = True
                for method_name, m_def in model_def.methods.items():
                    if "api.onchange" in m_def.decorators:
                        has_onchange = True

        for xml_k in xml_data:
            metrics["views"] += len(xml_k.views)
            metrics["security_rules"] += len(xml_k.security_rules)
            metrics["assets"] += len(xml_k.assets)

            if xml_k.views:
                has_views = True
            if xml_k.security_rules:
                has_security = True
            for view in xml_k.views:
                if view.view_type == "qweb":
                    has_qweb = True
            for action in xml_k.actions:
                if action.action_type == "ir.actions.report":
                    has_reports = True
                    metrics["reports"] += 1
            for record in xml_k.data_records:
                if record.model == "ir.cron":
                    has_cron = True
                    metrics["scheduled_actions"] += 1
                elif record.model == "mail.template":
                    has_mail = True

        if has_transient and has_views:
            scenarios.append(Scenario(name="Create Wizard", tags=["Wizard", "UI"]))

        if (has_controllers or has_routes) and has_qweb:
            scenarios.append(
                Scenario(name="Portal Interface", tags=["Portal", "Controller", "QWeb"])
            )
        elif has_controllers or has_routes:
            scenarios.append(Scenario(name="REST API / Controller", tags=["API", "Controller"]))

        if has_reports:
            scenarios.append(Scenario(name="Create Report", tags=["Report", "QWeb"]))

        if has_security:
            scenarios.append(
                Scenario(name="Complex Access Controls", tags=["Security", "Access Rights"])
            )

        if has_cron:
            scenarios.append(Scenario(name="Scheduled Automation", tags=["Automation", "Cron"]))

        if has_mail:
            scenarios.append(Scenario(name="Mail Template Automation", tags=["Mail", "Templates"]))

        if has_compute and has_onchange:
            scenarios.append(
                Scenario(name="Dynamic Business Logic", tags=["Compute", "Onchange", "Fields"])
            )

        if not scenarios:
            scenarios.append(Scenario(name="Module Architecture", tags=["Module", "Structural"]))

        # Enrich tags based on manifest and assign metrics
        depends = set(module.manifest.depends)
        for scenario in scenarios:
            scenario.metrics = metrics.copy()
            if "account" in depends:
                scenario.tags.append("Accounting")
            if "sale" in depends:
                scenario.tags.append("Sales")
            if "point_of_sale" in depends:
                scenario.tags.append("POS")
            if "mrp" in depends:
                scenario.tags.append("Manufacturing")
            if "stock" in depends:
                scenario.tags.append("Inventory")
            if "website" in depends:
                scenario.tags.append("Website")

        return scenarios
