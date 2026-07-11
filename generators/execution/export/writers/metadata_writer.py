"""Metadata writer for dataset export."""

import json
from generators.execution.export.writers.base_writer import BaseWriter
from generators.execution.export.enums import WriterType
from generators.execution.export.export_context import ExportContext


class MetadataWriter(BaseWriter):  # type: ignore[misc]
    """Writes the overarching dataset metadata file."""

    @property
    def writer_type(self) -> str:
        return WriterType.METADATA.value  # type: ignore[no-any-return]

    def generate_content(self, context: ExportContext) -> str:
        """Generate metadata content."""

        planning_result = context.planning_result
        planned_execution = planning_result.planned_execution if planning_result else None
        plan_id = planned_execution.plan_id if hasattr(planned_execution, 'plan_id') else "unknown"
        graph_id = planned_execution.graph_id if hasattr(planned_execution, 'graph_id') else "unknown"

        metadata_data = {
            "name": f"aiodoo-execution-dataset-{plan_id}",
            "description": "Auto-generated Execution Graph Dataset",
            "format": "jsonl",
            "source_graph": graph_id,
            "statistics": {},
        }
        
        if hasattr(context, "protocol_context") and context.protocol_context:
            metadata_data["protocol_hash"] = context.protocol_context.dataset.identifier.hash_value

        context.export_statistics.metadata_count += 1

        return json.dumps(metadata_data, sort_keys=True, ensure_ascii=False, indent=2)
