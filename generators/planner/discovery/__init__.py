"""
Discovery Layer for AIODOO Dataset Generator (Proxy).
"""

from aiodoo_datasets.generators.common.discovery.scanner import (
    ModuleScanner,
    OdooModule,
    ManifestInfo,
)
from aiodoo_datasets.generators.common.discovery.ast_parser import (
    OdooASTParser,
    PythonKnowledge,
    OdooModelDef,
    OdooFieldDef,
    OdooMethodDef,
    OdooRouteDef,
)
from aiodoo_datasets.generators.common.discovery.xml_parser import (
    OdooXMLParser,
    XMLKnowledge,
    OdooViewDef,
    OdooActionDef,
    OdooMenuDef,
    OdooSecurityDef,
    OdooAssetDef,
    OdooDataRecordDef,
)
from aiodoo_datasets.generators.common.discovery.classifier import ScenarioClassifier, Scenario

__all__ = [
    "ModuleScanner",
    "OdooModule",
    "ManifestInfo",
    "OdooASTParser",
    "PythonKnowledge",
    "OdooModelDef",
    "OdooFieldDef",
    "OdooMethodDef",
    "OdooRouteDef",
    "OdooXMLParser",
    "XMLKnowledge",
    "OdooViewDef",
    "OdooActionDef",
    "OdooMenuDef",
    "OdooSecurityDef",
    "OdooAssetDef",
    "OdooDataRecordDef",
    "ScenarioClassifier",
    "Scenario",
]
