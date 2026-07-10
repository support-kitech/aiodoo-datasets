"""Deterministic protocol serializer."""

import json
from dataclasses import asdict
from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import ExecutionProtocol
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext
from aiodoo_datasets.generators.execution.protocol.results.serializer_result import SerializerResult

class ProtocolSerializer:
    """Serializes the ExecutionProtocol into a deterministic JSON string."""
    
    @staticmethod
    def serialize(protocol: ExecutionProtocol, context: ProtocolContext) -> SerializerResult:
        """Serialize protocol deterministically."""
        try:
            # Convert frozen dataclass to dict
            protocol_dict = asdict(protocol)
            
            # Serialize with deterministic stable ordering
            serialized_data = json.dumps(
                protocol_dict,
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":")
            )
            
            context.protocol_statistics.serialization_count += 1
            context.protocol_statistics.protocol_size_bytes = len(serialized_data.encode("utf-8"))
            
            return SerializerResult(success=True, serialized_data=serialized_data)
        except Exception as e:
            return SerializerResult(success=False, diagnostics=(f"Serialization failed: {e}",))
