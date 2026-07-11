"""Enumerations for the Sources Framework domain models."""

from enum import Enum


class RepositoryType(Enum):
    """Supported repository types in the AIODOO ecosystem."""

    FRAMEWORK = "framework"
    COMMUNITY = "community"
    ENTERPRISE = "enterprise"
    OCA = "oca"
    DOCUMENTATION = "documentation"


class OdooVersion(Enum):
    """Supported Odoo versions."""

    V17 = "17.0"
    V18 = "18.0"
    V19 = "19.0"
