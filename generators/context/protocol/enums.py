"""Protocol Enums for Context Protocol V1."""

from enum import Enum


class ProtocolQueryType(str, Enum):
    """Protocol representation of query type."""

    FIND_MODEL = "find_model"
    FIND_FIELD = "find_field"
    FIND_COMPUTE = "find_compute"
    FIND_VIEW = "find_view"
    FIND_ACTION = "find_action"
    FIND_MENU = "find_menu"
    FIND_SECURITY = "find_security"
    FIND_DEPENDENCY = "find_dependency"


class ProtocolIntent(str, Enum):
    """Protocol representation of query intent."""

    FIND_MODEL = "locate_model_definition"
    FIND_FIELD = "locate_field_definition"
    FIND_COMPUTE = "locate_compute_logic"
    FIND_VIEW = "locate_view_displaying_element"
    FIND_ACTION = "locate_action_opening_element"
    FIND_MENU = "locate_menu_opening_element"
    FIND_SECURITY = "locate_security_protection"
    FIND_DEPENDENCY = "locate_module_dependencies"


class ProtocolNodeType(str, Enum):
    """Protocol representation of node type."""

    MODEL = "model"
    FIELD = "field"
    VIEW = "view"
    ACTION = "action"
    MENU = "menu"
    ACL = "acl"
    SECURITY_RULE = "security_rule"
    MANIFEST = "manifest"


class ProtocolLanguage(str, Enum):
    """Protocol representation of language."""

    PYTHON = "python"
    XML = "xml"
    CSV = "csv"
    JSON = "json"


class ProtocolRankingReason(str, Enum):
    """Protocol representation of ranking reason."""

    DIRECT_DEFINITION = "direct_definition"
    MODEL_INHERITANCE = "model_inheritance"
    MANIFEST_DEPENDENCY = "manifest_dependency"
    VIEW_REFERENCE = "view_reference"
    SECURITY_REFERENCE = "security_reference"
    ACTION_REFERENCE = "action_reference"
