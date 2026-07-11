"""Validator for execution protocol."""

from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)
from aiodoo_datasets.generators.execution.validation.schedule_protocol_validator import (
    ScheduleProtocolValidator,
)


class ExecutionProtocolValidator:
    """Validates ExecutionProtocol schema compliance."""

    @staticmethod
    def validate(protocol: ExecutionProtocol) -> tuple[str, ...]:
        violations = []
        if not protocol.plan_id:
            violations.append("ExecutionProtocol missing plan_id.")
        if not protocol.metadata:
            violations.append("ExecutionProtocol missing metadata.")
        if not protocol.schedules:
            violations.append(f"ExecutionProtocol {protocol.plan_id} has no schedules.")

        for schedule in protocol.schedules:
            violations.extend(ScheduleProtocolValidator.validate(schedule))

        return tuple(violations)
