"""Pipeline context for the Protocol Framework."""

from dataclasses import dataclass
from typing import Any

from protocol.pipeline.assembly_options import AssemblyOptions
from protocol.registry.registry import ProtocolRegistry


@dataclass(frozen=True, slots=True)
class PipelineContext:
    """
    Immutable context object passed through the assembly pipeline.
    Contains inputs, configuration, and registry.
    """

    # We use Any here to avoid coupling Protocol Framework directly to Preprocessing Framework
    # It will be a PreprocessedRepositoryContext at runtime
    input_context: Any
    options: AssemblyOptions
    registry: ProtocolRegistry
