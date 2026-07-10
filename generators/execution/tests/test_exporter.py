import unittest
import tempfile
from pathlib import Path
from types import MappingProxyType
from aiodoo_datasets.generators.execution.export.exporter import Exporter
from aiodoo_datasets.generators.execution.export.export_context import ExportContext
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics
from aiodoo_datasets.generators.execution.protocol.protocol_result import ProtocolResult
from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import ExecutionProtocol
from aiodoo_datasets.generators.execution.protocol.domain.metadata_protocol import MetadataProtocol
from aiodoo_datasets.generators.execution.protocol.protocol_statistics import ProtocolStatistics

class TestExporter(unittest.TestCase):
    def test_successful_export(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            metadata = MetadataProtocol("1.0", "1.0", "1.0", "time")
            protocol = ExecutionProtocol(plan_id="test_plan", graph_id="g1", metadata=metadata)
            
            ctx = ExportContext(
                protocol_result=ProtocolResult(success=True, protocol=protocol, serialized_data='{"plan_id":"test_plan"}'),
                protocol_statistics=ProtocolStatistics(),
                export_configuration=MappingProxyType({}),
                output_directory=Path(temp_dir),
                export_statistics=ExportStatistics()
            )
            
            result = Exporter.export(ctx)
            
            self.assertTrue(result.success)
            self.assertEqual(len(result.exported_files), 3)
            self.assertEqual(result.record_count, 1)
            
            jsonl_path = Path(temp_dir) / "test_plan.jsonl"
            manifest_path = Path(temp_dir) / "manifest.json"
            metadata_path = Path(temp_dir) / "metadata.json"
            
            self.assertTrue(jsonl_path.exists())
            self.assertTrue(manifest_path.exists())
            self.assertTrue(metadata_path.exists())

if __name__ == '__main__':
    unittest.main()
