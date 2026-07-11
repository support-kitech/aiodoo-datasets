"""Schema definition for the Context generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

CONTEXT_SCHEMA = DatasetSchema(
    schema_id="context-v1",
    generator_name="context",
    version="1.0.0",
    description="Context generator: id/query/artifacts/graph/metadata (ContextTask protocol)",
    top_level_fields=(
        FieldDefinition(name="id", field_type=str, required=True),
        FieldDefinition(name="query", field_type=dict, required=True),
        FieldDefinition(name="artifacts", field_type=list, required=True),
        FieldDefinition(name="graph", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module", "protocol_version"),
)
