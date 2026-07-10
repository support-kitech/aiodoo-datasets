"""Odoo edition definitions."""

from enum import Enum

class OdooEdition(Enum):
    """Available Odoo editions."""
    COMMUNITY = "community"
    ENTERPRISE = "enterprise"
    OCA = "oca"
