import unittest
import json
from pathlib import Path
from types import MappingProxyType
from generators.execution.export.writers.metadata_writer import MetadataWriter
from generators.execution.export.export_context import ExportContext
from generators.execution.export.export_statistics import ExportStatistics
from generators.execution.protocol.protocol_result import ProtocolResult
from generators.execution.protocol.domain.execution_protocol import (
    ExecutionProtocol,
)
from generators.execution.protocol.protocol_statistics import ProtocolStatistics


class TestMetadataWriter(unittest.TestCase):
    def test_generate_content(self) -> None:
        protocol = ExecutionProtocol(plan_id="p1", graph_id="g1", metadata=None)

        ctx = ExportContext(
            protocol_result=ProtocolResult(success=True, protocol=protocol),
            protocol_statistics=ProtocolStatistics(mapped_stages=5),
            export_configuration=MappingProxyType({}),
            output_directory=Path("/tmp"),
            export_statistics=ExportStatistics(),
        )

        writer = MetadataWriter()
        content = writer.generate_content(ctx)

        data = json.loads(content)
        self.assertEqual(data["name"], "aiodoo-execution-dataset-p1")
        self.assertEqual(data["source_graph"], "g1")
        self.assertEqual(data["statistics"]["mapped_stages"], 5)


if __name__ == "__main__":
    unittest.main()
