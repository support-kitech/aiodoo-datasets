"""Manifest writer for dataset export."""

import json
import hashlib
from aiodoo_datasets.generators.execution.export.writers.base_writer import BaseWriter
from aiodoo_datasets.generators.execution.export.enums import WriterType
from aiodoo_datasets.generators.execution.export.export_context import ExportContext


class ManifestWriter(BaseWriter):  # type: ignore[misc]
    """Writes the dataset manifest file."""

    @property
    def writer_type(self) -> str:
        return WriterType.MANIFEST.value  # type: ignore[no-any-return]

    def generate_content(self, context: ExportContext) -> str:
        """Generate deterministic manifest content."""

        # Calculate checksum over the raw serialized payload data
        data_bytes = context.protocol_result.serialized_data.encode("utf-8")
        checksum = hashlib.sha256(data_bytes).hexdigest()

        protocol = context.protocol_result.protocol
        metadata = protocol.metadata if protocol else None

        manifest_data = {
            "dataset_version": "1.0.0",
            "protocol_version": metadata.protocol_version if metadata else "unknown",
            "schema_version": metadata.schema_version if metadata else "unknown",
            "generator_version": "1.0.0",
            "generated_at": metadata.timestamp if metadata else "",
            "record_count": 1,
            "checksum": checksum,
            "exported_files": [f"{protocol.plan_id}.jsonl"] if protocol else [],
        }

        context.export_statistics.manifest_count += 1

        return json.dumps(manifest_data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
