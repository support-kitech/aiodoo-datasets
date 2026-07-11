"""Enums for the Planning Engine."""

from enum import Enum, unique


@unique
class PlanningStrategyType(Enum):
    """Available planning strategies."""

    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    DEPENDENCY = "DEPENDENCY"


@unique
class StageType(Enum):
    """Types of execution stages."""

    INITIALIZATION = "INITIALIZATION"
    PREPARATION = "PREPARATION"
    EXECUTION = "EXECUTION"
    VALIDATION = "VALIDATION"
    FINALIZATION = "FINALIZATION"
