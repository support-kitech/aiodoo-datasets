import unittest
from types import MappingProxyType
import json
from aiodoo_datasets.generators.execution.protocol.serializer import ProtocolSerializer
from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)
from aiodoo_datasets.generators.execution.protocol.domain.metadata_protocol import MetadataProtocol
from aiodoo_datasets.generators.execution.protocol.protocol_context import ProtocolContext
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics
from aiodoo_datasets.generators.execution.planning.planning_result import PlanningResult


class TestProtocolSerializer(unittest.TestCase):
    def test_deterministic_serialization(self) -> None:
        metadata = MetadataProtocol(
            protocol_version="1.0.0",
            schema_version="1.0",
            compatibility_version="1.0.0",
            timestamp="2026-07-10T12:00:00Z",
        )
        protocol = ExecutionProtocol(plan_id="p1", graph_id="g1", metadata=metadata, schedules=())

        ctx = ProtocolContext(
            planning_result=PlanningResult(success=True),
            planning_statistics=None,
            configuration=MappingProxyType({}),
            protocol_version="1.0.0",
            protocol_statistics=ProtocolStatistics(),
        )

        res1 = ProtocolSerializer.serialize(protocol, ctx)
        self.assertTrue(res1.success)

        res2 = ProtocolSerializer.serialize(protocol, ctx)
        self.assertEqual(res1.serialized_data, res2.serialized_data)

        # Verify valid JSON
        data = json.loads(res1.serialized_data)
        self.assertEqual(data["plan_id"], "p1")
        self.assertEqual(data["graph_id"], "g1")


if __name__ == "__main__":
    unittest.main()
