"""
Discovery Layer for AIODOO Dataset Generator.

Responsible for safely scanning and parsing Odoo source code into structured 
engineering knowledge representations (AST and XML structure), and classifying 
those structures into AIODOO training scenarios.

Features robust caching, strongly typed manifests, and deep multidimensional 
heuristics for production-grade dataset generation.
"""

from .scanner import ModuleScanner, OdooModule, ManifestInfo
from .ast_parser import (
    OdooASTParser, PythonKnowledge, OdooModelDef, OdooFieldDef, 
    OdooMethodDef, OdooRouteDef
)
from .xml_parser import (
    OdooXMLParser, XMLKnowledge, OdooViewDef, OdooActionDef, 
    OdooMenuDef, OdooSecurityDef, OdooAssetDef, OdooDataRecordDef
)
from .classifier import ScenarioClassifier, Scenario

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
