from enum import Enum, auto


class BuilderState(Enum):
    """
    Tracks the lifecycle state of a Builder.
    Critical for ensuring deterministic execution and preventing side-effects
    in future multiprocessing/distributed orchestration.
    """

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    SKIPPED = auto()
