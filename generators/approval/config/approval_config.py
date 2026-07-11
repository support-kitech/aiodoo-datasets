"""Approval config module."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApprovalConfig:
    """Configuration for the approval generator."""

    output_dir: str
    manifest_path: str
    fail_on_validation: bool = True
    strict_mode: bool = False
