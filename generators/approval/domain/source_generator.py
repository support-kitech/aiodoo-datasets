"""Source generator enumeration."""

from enum import Enum


class SourceGenerator(str, Enum):
    """The source generator producing the evidence."""

    PLANNER = "PLANNER"
    CODING = "CODING"
    REPAIR = "REPAIR"
    CONTEXT = "CONTEXT"
    EXECUTION = "EXECUTION"
    APPROVAL = "APPROVAL"
    CONVERSATION = "CONVERSATION"
    EVALUATION = "EVALUATION"
