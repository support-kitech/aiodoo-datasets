import unittest
import json
import hashlib
from pathlib import Path
from types import MappingProxyType
from aiodoo_datasets.generators.execution.export.writers.manifest_writer import ManifestWriter
from aiodoo_datasets.generators.execution.export.export_context import ExportContext
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics
from aiodoo_datasets.generators.execution.protocol.protocol_result import ProtocolResult
from aiodoo_datasets.generators.execution.protocol.domain.execution_protocol import ExecutionProtocol
from aiodoo_datasets.generators.execution.protocol.domain.metadata_protocol import MetadataProtocol

class TestManifestWriter(unittest.TestCase):
    def test_generate_content(self):
        metadata = MetadataProtocol("1.0", "1.0", "1.0", "time")
        protocol = ExecutionProtocol(plan_id="p1", graph_id="g1", metadata=metadata)
        
        ctx = ExportContext(
            protocol_result=ProtocolResult(success=True, protocol=protocol, serialized_data='{"test": 1}'),
            protocol_statistics=None,
            export_configuration=MappingProxyType({}),
            output_directory=Path("/tmp"),
            export_statistics=ExportStatistics()
        )
        
        writer = ManifestWriter()
        content = writer.generate_content(ctx)
        
        data = json.loads(content)
        self.assertEqual(data["dataset_version"], "1.0.0")
        self.assertEqual(data["record_count"], 1)
        
        expected_checksum = hashlib.sha256(b'{"test": 1}').hexdigest()
        self.assertEqual(data["checksum"], expected_checksum)

if __name__ == '__main__':
    unittest.main()
