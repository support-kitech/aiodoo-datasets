"""Assembly options for the Protocol Framework pipeline."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssemblyOptions:
    """
    Immutable configuration options for protocol assembly.
    """

    validate_schema: bool = True
    export_format: str = "json"
    verbose: bool = False
    quiet: bool = False
