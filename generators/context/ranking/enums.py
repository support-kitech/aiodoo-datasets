"""Enumerations for Ranking Engine."""

from enum import Enum

class RankingRuleType(str, Enum):
    """Enumeration of all supported ranking rule types."""
    DEFINITION = "definition"
    INHERITANCE = "inheritance"
    DEPENDENCY = "dependency"
    SECURITY = "security"
    VIEW = "view"
    ACTION = "action"

from enum import IntEnum

class RankingScore(IntEnum):
    """Determines strict deterministic score value for rules."""
    DEFINITION = 100
    INHERITANCE = 90
    DEPENDENCY = 80
    VIEW = 70
    SECURITY = 70
    ACTION = 60

class RankingReason(str, Enum):
    """Canonical reasons for a ranking decision."""
    DIRECT_DEFINITION = "direct_definition"
    MODEL_INHERITANCE = "model_inheritance"
    MANIFEST_DEPENDENCY = "manifest_dependency"
    VIEW_REFERENCE = "view_reference"
    SECURITY_REFERENCE = "security_reference"
    ACTION_REFERENCE = "action_reference"
