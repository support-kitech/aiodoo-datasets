"""Protocol pipeline orchestrator."""

from generators.execution.protocol.protocol_context import ProtocolContext
from generators.execution.protocol.protocol_result import ProtocolResult
from generators.execution.protocol.mappers.protocol_mapper import ProtocolMapper
from generators.execution.validation.protocol_validator import ProtocolValidator
from generators.execution.protocol.serializer import ProtocolSerializer


class Protocol:
    """
    Orchestrates the protocol pipeline:
    Planning Result -> Protocol Mapper -> Protocol Validation -> Protocol Serialization
    """

    @staticmethod
    def map_protocol(context: ProtocolContext) -> ProtocolResult:
        """Execute the protocol pipeline."""

        # 1. Map to Protocol Domain
        mapper_result = ProtocolMapper.map(context)
        if not mapper_result.success or not mapper_result.protocol:
            return ProtocolResult(success=False, diagnostics=mapper_result.diagnostics)

        # 2. Validate Protocol Domain
        validation_result = ProtocolValidator.validate(mapper_result.protocol)
        if not validation_result.success:
            return ProtocolResult(
                success=False,
                protocol=mapper_result.protocol,
                diagnostics=validation_result.violations,
            )

        context.protocol_statistics.validation_count += 1

        # 3. Serialize
        serializer_result = ProtocolSerializer.serialize(mapper_result.protocol, context)
        if not serializer_result.success:
            return ProtocolResult(
                success=False,
                protocol=mapper_result.protocol,
                diagnostics=serializer_result.diagnostics,
            )

        return ProtocolResult(
            success=True,
            protocol=mapper_result.protocol,
            serialized_data=serializer_result.serialized_data,
        )
