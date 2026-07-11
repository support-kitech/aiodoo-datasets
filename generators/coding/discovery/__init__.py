"""Discovery layer for the Coding Generator.
Reuses the shared implementation from the Common Generator framework to guarantee identical parsing and version compatibility.
"""

from generators.common.discovery.ast_parser import OdooASTParser, PythonKnowledge
from generators.common.discovery.xml_parser import OdooXMLParser, XMLKnowledge
from generators.common.discovery.classifier import ScenarioClassifier, Scenario

__all__ = [
    "OdooASTParser",
    "PythonKnowledge",
    "OdooXMLParser",
    "XMLKnowledge",
    "ScenarioClassifier",
    "Scenario",
]
