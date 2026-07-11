"""
Discovery Layer for AIODOO Dataset Generator (Proxy).
"""

from generators.common.discovery.ast_parser import (
    OdooASTParser,
    PythonKnowledge,
    OdooModelDef,
    OdooFieldDef,
    OdooMethodDef,
    OdooRouteDef,
)
from generators.common.discovery.xml_parser import (
    OdooXMLParser,
    XMLKnowledge,
    OdooViewDef,
    OdooActionDef,
    OdooMenuDef,
    OdooSecurityDef,
    OdooAssetDef,
    OdooDataRecordDef,
)
from generators.common.discovery.classifier import ScenarioClassifier, Scenario

__all__ = [
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
