"""Parses XML files to extract structured Odoo views and actions."""

import logging
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class OdooViewDef:
    id: str
    model: str
    view_type: str
    inherit_id: str | None = None


@dataclass(slots=True)
class OdooActionDef:
    id: str
    action_type: str
    model: str = ""


@dataclass(slots=True)
class OdooMenuDef:
    id: str
    name: str = ""
    parent: str = ""
    action: str = ""


@dataclass(slots=True)
class OdooSecurityDef:
    id: str
    model: str = ""
    type: str = "ir.model.access"


@dataclass(slots=True)
class OdooAssetDef:
    id: str
    inherit_id: str


@dataclass(slots=True)
class OdooDataRecordDef:
    id: str
    model: str


@dataclass(slots=True)
class XMLKnowledge:
    """Represents extracted structural knowledge from XML files."""

    views: list[OdooViewDef] = field(default_factory=list)
    actions: list[OdooActionDef] = field(default_factory=list)
    menus: list[OdooMenuDef] = field(default_factory=list)
    security_rules: list[OdooSecurityDef] = field(default_factory=list)
    assets: list[OdooAssetDef] = field(default_factory=list)
    data_records: list[OdooDataRecordDef] = field(default_factory=list)


class ModuleKnowledgeList(list):  # type: ignore[type-arg]
    """Backwards compatible list that also holds a .files attribute mapping path -> knowledge."""

    def __init__(self, items=None, files_dict=None) -> None:  # type: ignore[no-untyped-def]
        super().__init__(items or [])
        self.files = files_dict or {}


class OdooXMLParser:
    """Parses Odoo XML/CSV files."""

    def parse_module(self, module_path: Path):  # type: ignore[no-untyped-def]
        results = []  # type: ignore[var-annotated]
        files_dict = {}  # type: ignore[var-annotated]
        if not module_path.is_dir():
            return ModuleKnowledgeList(results, files_dict)

        global_knowledge = XMLKnowledge()

        for xml_file in module_path.rglob("*.xml"):
            file_knowledge = XMLKnowledge()
            self._parse_xml_file(xml_file, file_knowledge)

            global_knowledge.views.extend(file_knowledge.views)
            global_knowledge.actions.extend(file_knowledge.actions)
            global_knowledge.menus.extend(file_knowledge.menus)
            global_knowledge.security_rules.extend(file_knowledge.security_rules)
            global_knowledge.assets.extend(file_knowledge.assets)
            global_knowledge.data_records.extend(file_knowledge.data_records)

            rel_path = str(xml_file.relative_to(module_path))
            files_dict[rel_path] = file_knowledge

        for csv_file in module_path.rglob("*.csv"):
            if "ir.model.access" in csv_file.name:
                sec_def = OdooSecurityDef(id=csv_file.name, type="ir.model.access")
                global_knowledge.security_rules.append(sec_def)

                file_knowledge = XMLKnowledge()
                file_knowledge.security_rules.append(sec_def)
                rel_path = str(csv_file.relative_to(module_path))
                files_dict[rel_path] = file_knowledge

        if any(
            [
                global_knowledge.views,
                global_knowledge.actions,
                global_knowledge.menus,
                global_knowledge.security_rules,
                global_knowledge.assets,
                global_knowledge.data_records,
            ]
        ):
            results.append(global_knowledge)

        return ModuleKnowledgeList(results, files_dict)

    def _parse_xml_file(self, file_path: Path, knowledge: XMLKnowledge) -> None:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            for record in root.findall(".//record"):
                model = record.get("model")
                record_id = record.get("id", "")

                if model == "ir.ui.view":
                    view_type = self._extract_field(record, "type", default="unknown")
                    if view_type == "unknown":
                        arch = record.find(".//field[@name='arch']")
                        if arch is not None and len(arch) > 0:
                            view_type = arch[0].tag

                    inherit_id = None
                    inherit_node = record.find(".//field[@name='inherit_id']")
                    if inherit_node is not None:
                        inherit_id = inherit_node.get("ref")

                    model_name = self._extract_field(record, "model")
                    knowledge.views.append(
                        OdooViewDef(
                            id=record_id,
                            model=model_name,
                            view_type=view_type,
                            inherit_id=inherit_id,
                        )
                    )

                elif model and model.startswith("ir.actions."):
                    res_model = self._extract_field(record, "res_model")
                    knowledge.actions.append(
                        OdooActionDef(id=record_id, action_type=model, model=res_model)
                    )

                elif model == "ir.rule":
                    model_id = self._extract_field(record, "model_id")
                    knowledge.security_rules.append(
                        OdooSecurityDef(id=record_id, model=model_id, type="ir.rule")
                    )
                elif model == "res.groups":
                    knowledge.security_rules.append(
                        OdooSecurityDef(id=record_id, type="res.groups")
                    )
                elif model:
                    knowledge.data_records.append(OdooDataRecordDef(id=record_id, model=model))

            for menu in root.findall(".//menuitem"):
                knowledge.menus.append(
                    OdooMenuDef(
                        id=menu.get("id", ""),
                        name=menu.get("name", ""),
                        parent=menu.get("parent", ""),
                        action=menu.get("action", ""),
                    )
                )

            for template in root.findall(".//template"):
                inherit_id = template.get("inherit_id")
                if inherit_id and "assets_" in inherit_id:
                    knowledge.assets.append(
                        OdooAssetDef(id=template.get("id", ""), inherit_id=inherit_id)
                    )

        except ET.ParseError as exc:
            logger.debug("XML parse error in %s: %s", file_path, exc)
        except Exception as exc:
            logger.debug("Failed to parse %s: %s", file_path, exc)

    def _extract_field(self, record: ET.Element, name: str, default: str = "") -> str:
        field_node = record.find(f".//field[@name='{name}']")
        if field_node is not None and field_node.text:
            return field_node.text.strip()
        return default
