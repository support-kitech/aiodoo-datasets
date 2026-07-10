"""Batch validator."""

from aiodoo_datasets.generators.execution.planning.domain.execution_batch import ExecutionBatch
from aiodoo_datasets.generators.execution.validation.phase_validator import PhaseValidator

class BatchValidator:
    """Validator for execution batches."""
    
    @staticmethod
    def validate(batch: ExecutionBatch) -> tuple[str, ...]:
        """Validate a batch and its phases."""
        violations = []
        if not batch.batch_id:
            violations.append("Batch has no batch_id.")
        if not batch.phases:
            violations.append(f"Batch {batch.batch_id} has no phases.")
            
        for phase in batch.phases:
            violations.extend(PhaseValidator.validate(phase))
            
        return tuple(violations)
