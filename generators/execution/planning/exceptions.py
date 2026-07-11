"""Exceptions for the Planning Engine."""


class PlanningError(Exception):
    """Base exception for planning errors."""

    pass


class InvalidStageError(PlanningError):
    """Raised when a stage is invalid."""

    pass


class InvalidPhaseError(PlanningError):
    """Raised when a phase is invalid."""

    pass


class InvalidBatchError(PlanningError):
    """Raised when a batch is invalid."""

    pass


class ScheduleError(PlanningError):
    """Raised when a schedule cannot be formed."""

    pass
