"""Metadata writer for dataset export."""

import json
from aiodoo_datasets.generators.execution.export.writers.base_writer import BaseWriter
from aiodoo_datasets.generators.execution.export.enums import WriterType
from aiodoo_datasets.generators.execution.export.export_context import ExportContext

class MetadataWriter(BaseWriter):
    """Writes the overarching dataset metadata file."""

    @property
    def writer_type(self) -> str:
        return WriterType.METADATA.value

    def generate_content(self, context: ExportContext) -> str:
        """Generate metadata content."""
        
        protocol = context.protocol_result.protocol
        
        metadata_data = {
            "name": f"aiodoo-execution-dataset-{protocol.plan_id}" if protocol else "unknown",
            "description": "Auto-generated Execution Graph Dataset",
            "format": "jsonl",
            "source_graph": protocol.graph_id if protocol else "unknown",
            "statistics": {
                "mapped_stages": context.protocol_statistics.mapped_stages,
                "mapped_phases": context.protocol_statistics.mapped_phases,
                "mapped_batches": context.protocol_statistics.mapped_batches,
                "mapped_schedules": context.protocol_statistics.mapped_schedules
            }
        }
        
        context.export_statistics.metadata_count += 1
        
        return json.dumps(
            metadata_data,
            sort_keys=True,
            ensure_ascii=False,
            indent=2
        )
