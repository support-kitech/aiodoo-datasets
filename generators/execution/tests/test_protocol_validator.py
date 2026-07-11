import unittest
from generators.execution.validation.protocol_validator import ProtocolValidator
from generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)
from generators.execution.protocol.domain.metadata_protocol import MetadataProtocol
from generators.execution.protocol.domain.schedule_protocol import ScheduleProtocol


class TestProtocolValidator(unittest.TestCase):
    def test_validation(self) -> None:
        metadata = MetadataProtocol(
            protocol_version="1.0.0", schema_version="1.0", compatibility_version="1.0.0"
        )

        # Valid empty schedule
        sch = ScheduleProtocol(schedule_id="s1", strategy="seq", batches=())
        # The validator requires at least one schedule
        # The schema might require batches, let's see. The validator says:
        # if not schedule.batches: violations.append("... has no batches")
        # So we expect violations.

        protocol = ExecutionProtocol(
            plan_id="p1", graph_id="g1", metadata=metadata, schedules=(sch,)
        )

        res = ProtocolValidator.validate(protocol)
        self.assertFalse(res.success)
        self.assertTrue(len(res.violations) > 0)
        self.assertIn("has no batches", res.violations[0])


if __name__ == "__main__":
    unittest.main()
