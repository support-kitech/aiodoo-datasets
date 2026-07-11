"""Assembly Options for the Protocol Pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssemblyOptions:
    """Options governing the assembly of Protocol objects."""
    
    strict_validation: bool = True
    fail_fast: bool = True
