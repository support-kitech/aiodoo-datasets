"""Protocol Validator for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.exceptions import EvaluationValidationError
from aiodoo_datasets.generators.evaluation.protocol.domain.benchmark_protocol import EvaluationProtocol

class ProtocolValidator:
    """Validates serialized protocol objects without mutating them."""
    
    @staticmethod
    def validate(protocol: EvaluationProtocol) -> None:
        """Fail-fast validation of the protocol schema."""
        if not protocol:
            raise EvaluationValidationError("Evaluation protocol cannot be empty.")
            
        if not protocol.evaluation_id.startswith("EVALROOT-"):
            raise EvaluationValidationError(f"Invalid Evaluation protocol ID: {protocol.evaluation_id}")
            
        if not protocol.catalog:
            raise EvaluationValidationError("Protocol must contain a BenchmarkCatalog.")
