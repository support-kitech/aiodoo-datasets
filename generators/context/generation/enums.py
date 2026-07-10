"""Enumerations for Query Framework."""

from enum import Enum

class QueryType(str, Enum):
    """Enumeration of all supported query intents."""
    FIND_MODEL = "find_model"
    FIND_FIELD = "find_field"
    FIND_COMPUTE = "find_compute"
    FIND_VIEW = "find_view"
    FIND_ACTION = "find_action"
    FIND_MENU = "find_menu"
    FIND_SECURITY = "find_security"
    FIND_DEPENDENCY = "find_dependency"

class QueryIntent(str, Enum):
    """Enumeration of specific engineering intents."""
    FIND_MODEL = "locate_model_definition"
    FIND_FIELD = "locate_field_definition"
    FIND_COMPUTE = "locate_compute_logic"
    FIND_VIEW = "locate_view_displaying_element"
    FIND_ACTION = "locate_action_opening_element"
    FIND_MENU = "locate_menu_opening_element"
    FIND_SECURITY = "locate_security_protection"
    FIND_DEPENDENCY = "locate_module_dependencies"
