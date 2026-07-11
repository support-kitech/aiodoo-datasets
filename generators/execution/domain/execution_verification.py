"""Immutable representation of execution success validation."""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class ExecutionVerification:
    """
    Defines commands or checks to assert step success.

    Attributes:
        command: The shell command or Python script to execute.
        expected_output: Optional string expected in the standard output.
    """

    command: str
    expected_output: str | None = None
