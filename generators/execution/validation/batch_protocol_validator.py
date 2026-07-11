"""Validator for batch protocol."""

from aiodoo_datasets.generators.execution.protocol.domain.batch_protocol import BatchProtocol
from aiodoo_datasets.generators.execution.validation.phase_protocol_validator import (
    PhaseProtocolValidator,
)


class BatchProtocolValidator:
    """Validates BatchProtocol schema compliance."""

    @staticmethod
    def validate(batch: BatchProtocol) -> tuple[str, ...]:
        violations = []
        if not batch.batch_id:
            violations.append("BatchProtocol missing batch_id.")
        if not batch.phases:
            violations.append(f"BatchProtocol {batch.batch_id} has no phases.")

        for phase in batch.phases:
            violations.extend(PhaseProtocolValidator.validate(phase))

        return tuple(violations)
