"""Mapper result objects."""

from dataclasses import dataclass
from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import ExecutionProtocol

@dataclass(frozen=True, slots=True)
class MapperResult:
    """
    Immutable result from ProtocolMapper.
    
    Attributes:
        success: Whether the mapping was successful.
        protocol: The mapped ExecutionProtocol.
        diagnostics: Any diagnostic messages.
    """
    success: bool
    protocol: ExecutionProtocol | None = None
    diagnostics: tuple[str, ...] = tuple()
