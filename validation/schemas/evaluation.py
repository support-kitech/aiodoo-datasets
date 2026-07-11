"""Schema definition for the Evaluation generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

EVALUATION_SCHEMA = DatasetSchema(
    schema_id="evaluation-v1",
    generator_name="evaluation",
    version="1.0.0",
    description="Evaluation generator: evaluation_id/catalog/metadata",
    top_level_fields=(
        FieldDefinition(name="evaluation_id", field_type=str, required=True),
        FieldDefinition(name="catalog", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_version", "schema_version"),
)
