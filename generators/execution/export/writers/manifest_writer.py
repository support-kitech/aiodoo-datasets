"""Manifest writer for dataset export."""

import json
import hashlib
from generators.execution.export.writers.base_writer import BaseWriter
from generators.execution.export.enums import WriterType
from generators.execution.export.export_context import ExportContext


class ManifestWriter(BaseWriter):  # type: ignore[misc]
    """Writes the dataset manifest file."""

    @property
    def writer_type(self) -> str:
        return WriterType.MANIFEST.value  # type: ignore[no-any-return]

    def generate_content(self, context: ExportContext) -> str:
        """Generate deterministic manifest content."""

        import dataclasses

        planning_result = context.planning_result
        planned_execution = planning_result.planned_execution if planning_result else None

        data = dataclasses.asdict(planned_execution) if planned_execution else {}
        if hasattr(context, "protocol_context") and context.protocol_context:
            data["protocol_hash"] = context.protocol_context.dataset.identifier.hash_value

        data_bytes = json.dumps(data).encode("utf-8")
        checksum = hashlib.sha256(data_bytes).hexdigest()

        plan_id = planned_execution.plan_id if hasattr(planned_execution, "plan_id") else "unknown"

        manifest_data = {
            "dataset_version": "1.0.0",
            "protocol_version": "1.0.0",
            "schema_version": "1.0.0",
            "generator_version": "1.0.0",
            "generated_at": "",
            "record_count": 1,
            "checksum": checksum,
            "exported_files": [f"{plan_id}.jsonl"],
        }

        context.export_statistics.manifest_count += 1

        return json.dumps(manifest_data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
