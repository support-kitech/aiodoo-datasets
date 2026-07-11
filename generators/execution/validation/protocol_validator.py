"""Protocol validator orchestrator."""

from generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)
from generators.execution.validation.execution_protocol_validator import (
    ExecutionProtocolValidator,
)
from generators.execution.protocol.results.validation_result import ValidationResult


class ProtocolValidator:
    """Orchestrates validation of the mapped protocol object."""

    @staticmethod
    def validate(protocol: ExecutionProtocol) -> ValidationResult:
        """Validate the full execution protocol."""
        violations = ExecutionProtocolValidator.validate(protocol)

        if violations:
            return ValidationResult(success=False, violations=violations)

        return ValidationResult(success=True)
