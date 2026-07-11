"""Validator for schedule protocol."""

from generators.execution.protocol.domain.schedule_protocol import ScheduleProtocol
from generators.execution.validation.batch_protocol_validator import (
    BatchProtocolValidator,
)


class ScheduleProtocolValidator:
    """Validates ScheduleProtocol schema compliance."""

    @staticmethod
    def validate(schedule: ScheduleProtocol) -> tuple[str, ...]:
        violations = []
        if not schedule.schedule_id:
            violations.append("ScheduleProtocol missing schedule_id.")
        if not schedule.batches:
            violations.append(f"ScheduleProtocol {schedule.schedule_id} has no batches.")

        for batch in schedule.batches:
            violations.extend(BatchProtocolValidator.validate(batch))

        return tuple(violations)
