"""Schema definition for the Approval generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

APPROVAL_SCHEMA = DatasetSchema(
    schema_id="approval-v1",
    generator_name="approval",
    version="1.0.0",
    description="Approval generator: review_id/decision/findings/evidence/recommendations/metadata",
    top_level_fields=(
        FieldDefinition(name="review_id", field_type=str, required=True),
        FieldDefinition(name="decision", field_type=dict, required=True),
        FieldDefinition(name="findings", field_type=list, required=True),
        FieldDefinition(name="evidence", field_type=list, required=True),
        FieldDefinition(name="recommendations", field_type=list, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_version", "schema_version"),
)
