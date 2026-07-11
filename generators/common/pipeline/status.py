from enum import Enum, auto


class PipelineStatus(Enum):
    """Lifecycle states for pipeline execution."""

    SUCCESS = auto()
    SKIPPED = auto()
    FAILED = auto()
