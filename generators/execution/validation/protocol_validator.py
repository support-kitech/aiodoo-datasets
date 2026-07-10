"""Protocol validator orchestrator."""

from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import ExecutionProtocol
from aiodoo_datasets.generators.execution.validation.execution_protocol_validator import ExecutionProtocolValidator
from aiodoo_datasets.generators.execution.protocol.results.validation_result import ValidationResult

class ProtocolValidator:
    """Orchestrates validation of the mapped protocol object."""
    
    @staticmethod
    def validate(protocol: ExecutionProtocol) -> ValidationResult:
        """Validate the full execution protocol."""
        violations = ExecutionProtocolValidator.validate(protocol)
        
        if violations:
            return ValidationResult(success=False, violations=violations)
            
        return ValidationResult(success=True)
