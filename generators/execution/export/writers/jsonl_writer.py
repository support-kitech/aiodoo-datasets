"""JSONL writer for dataset export."""

from generators.execution.export.writers.base_writer import BaseWriter
from generators.execution.export.enums import WriterType
from generators.execution.export.export_context import ExportContext


class JSONLWriter(BaseWriter):  # type: ignore[misc]
    """Writes the dataset payload as a JSON Lines file."""

    @property
    def writer_type(self) -> str:
        return WriterType.JSONL.value  # type: ignore[no-any-return]

    def generate_content(self, context: ExportContext) -> str:
        """
        Generate JSONL content.
        Since we currently only support exporting a single ExecutionProtocol per graph,
        we just return its serialized string with a newline.
        """
        import json
        import dataclasses

        context.export_statistics.jsonl_records += 1

        data = {}
        if context.planning_result and context.planning_result.planned_execution:
            data = dataclasses.asdict(context.planning_result.planned_execution)
            if hasattr(context, "protocol_context") and context.protocol_context:
                data["protocol_hash"] = context.protocol_context.dataset.identifier.hash_value

        return f"{json.dumps(data)}\n"
