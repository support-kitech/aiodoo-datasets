"""Protocol pipeline result."""

from dataclasses import dataclass
from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)


@dataclass(frozen=True, slots=True)
class ProtocolResult:
    """
    Immutable result from the Protocol pipeline.

    Attributes:
        success: Whether the pipeline completed successfully.
        protocol: The mapped and validated ExecutionProtocol.
        serialized_data: The JSON serialized string of the protocol.
        diagnostics: Any diagnostic messages.
    """

    success: bool
    protocol: ExecutionProtocol | None = None
    serialized_data: str = ""
    diagnostics: tuple[str, ...] = tuple()
