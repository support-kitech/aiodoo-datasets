import unittest
import tempfile
from pathlib import Path
from types import MappingProxyType
from aiodoo_datasets.generators.execution.export.writers.base_writer import BaseWriter
from aiodoo_datasets.generators.execution.export.export_context import ExportContext
from aiodoo_datasets.generators.execution.export.export_statistics import ExportStatistics
from aiodoo_datasets.generators.execution.protocol.protocol_result import ProtocolResult


class DummyWriter(BaseWriter):
    @property
    def writer_type(self) -> str:
        return "DUMMY"

    def generate_content(self, context: ExportContext) -> str:
        return "test content"


class TestAtomicExport(unittest.TestCase):
    def test_atomic_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir) / "test.txt"

            ctx = ExportContext(
                protocol_result=ProtocolResult(success=True),
                protocol_statistics=None,
                export_configuration=MappingProxyType({}),
                output_directory=Path(temp_dir),
                export_statistics=ExportStatistics(),
            )

            writer = DummyWriter()
            writer.write(target_path, ctx)

            self.assertTrue(target_path.exists())
            self.assertEqual(target_path.read_text(), "test content")
            self.assertEqual(ctx.export_statistics.exported_files, 1)


if __name__ == "__main__":
    unittest.main()
