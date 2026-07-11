"""Discovery layer for the Coding Generator.
Reuses the shared implementation from the Common Generator framework to guarantee identical parsing and version compatibility.
"""

from aiodoo_datasets.generators.common.discovery.scanner import (
    ModuleScanner,
    OdooModule,
    ManifestInfo,
)
from aiodoo_datasets.generators.common.discovery.ast_parser import OdooASTParser, PythonKnowledge
from aiodoo_datasets.generators.common.discovery.xml_parser import OdooXMLParser, XMLKnowledge
from aiodoo_datasets.generators.common.discovery.classifier import ScenarioClassifier, Scenario

__all__ = [
    "ModuleScanner",
    "OdooModule",
    "ManifestInfo",
    "OdooASTParser",
    "PythonKnowledge",
    "OdooXMLParser",
    "XMLKnowledge",
    "ScenarioClassifier",
    "Scenario",
]
