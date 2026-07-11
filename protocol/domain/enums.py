"""Enumerations for the Protocol Framework."""

from enum import Enum


class ProtocolType(Enum):
    """The types of Protocol objects."""

    DATASET = "dataset"
    MANIFEST = "manifest"
    SCHEMA = "schema"
    METADATA = "metadata"
    REFERENCE = "reference"
    RELATIONSHIP = "relationship"
    VERSION = "version"


class RelationshipType(Enum):
    """Common relationships between protocol objects."""

    PARENT = "parent"
    CHILD = "child"
    DEPENDS_ON = "depends_on"
    REFERENCES = "references"
    EXTENDS = "extends"
    ASSOCIATED_WITH = "associated_with"


class ReferenceType(Enum):
    """The type of target a ProtocolReference points to."""

    REPOSITORY = "repository"
    MODULE = "module"
    FILE = "file"
    DATASET = "dataset"
    ARTIFACT = "artifact"
    CONVERSATION = "conversation"
    EVALUATION = "evaluation"
    GENERATOR = "generator"


class ExportFormat(Enum):
    """Supported export formats for protocol objects."""

    JSON = "json"
    JSONL = "jsonl"
    DICT = "dict"
