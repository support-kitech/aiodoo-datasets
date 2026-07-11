"""Verification knowledge container."""

from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class VerificationKnowledge:
    """Extracted assertion strategy for operation success."""

    operation_ref: str
    command_strategy: str
    expected_output: str | None = None
