import unittest
from pathlib import Path
from types import MappingProxyType
from generators.execution.export.writers.jsonl_writer import JSONLWriter
from generators.execution.export.export_context import ExportContext
from generators.execution.export.export_statistics import ExportStatistics
from generators.execution.protocol.protocol_result import ProtocolResult


class TestJSONLWriter(unittest.TestCase):
    def test_generate_content(self) -> None:
        ctx = ExportContext(
            protocol_result=ProtocolResult(success=True, serialized_data='{"plan_id":"p1"}'),
            protocol_statistics=None,
            export_configuration=MappingProxyType({}),
            output_directory=Path("/tmp"),
            export_statistics=ExportStatistics(),
        )

        writer = JSONLWriter()
        content = writer.generate_content(ctx)

        self.assertEqual(content, '{"plan_id":"p1"}\n')
        self.assertEqual(ctx.export_statistics.jsonl_records, 1)


if __name__ == "__main__":
    unittest.main()
