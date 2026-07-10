"""Enums for artifact types."""

from enum import Enum

class PythonArtifactType(Enum):
    MODEL = "model"
    FIELD = "field"
    METHOD = "method"
    CONTROLLER = "controller"
    TEST = "test"
    INIT = "init"

class XMLArtifactType(Enum):
    VIEW = "view"
    ACTION = "action"
    MENU = "menu"
    TEMPLATE = "template"
    RECORD = "record"

class CSVArtifactType(Enum):
    ACCESS_RIGHT = "access_right"
    DATA = "data"
