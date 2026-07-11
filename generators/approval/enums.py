"""Enums for the Approval Generator."""

from enum import Enum


class DecisionEnum(str, Enum):
    """The final verdict for a generated implementation."""

    APPROVED = "APPROVED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    REJECTED = "REJECTED"


class ConfidenceLevel(str, Enum):
    """The confidence score classification of the review."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Severity(str, Enum):
    """The severity of a specific finding."""

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class RuleCategory(str, Enum):
    """The classification category of a review rule."""

    ARCHITECTURE = "ARCHITECTURE"
    SECURITY = "SECURITY"
    PERFORMANCE = "PERFORMANCE"
    STYLE = "STYLE"
    ODOO = "ODOO"
    PROTOCOL = "PROTOCOL"
    TESTING = "TESTING"
    DOCUMENTATION = "DOCUMENTATION"
    MIGRATION = "MIGRATION"
