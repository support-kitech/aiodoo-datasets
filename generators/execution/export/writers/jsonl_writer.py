"""JSONL writer for dataset export."""

from aiodoo_datasets.generators.execution.export.writers.base_writer import BaseWriter
from aiodoo_datasets.generators.execution.export.enums import WriterType
from aiodoo_datasets.generators.execution.export.export_context import ExportContext


class JSONLWriter(BaseWriter):
    """Writes the dataset payload as a JSON Lines file."""

    @property
    def writer_type(self) -> str:
        return WriterType.JSONL.value

    def generate_content(self, context: ExportContext) -> str:
        """
        Generate JSONL content.
        Since we currently only support exporting a single ExecutionProtocol per graph,
        we just return its serialized string with a newline.
        """
        context.export_statistics.jsonl_records += 1
        return f"{context.protocol_result.serialized_data}\n"
