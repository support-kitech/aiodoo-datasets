"""Schema definition for the Approval generator dataset (subject-decision grain)."""

from validation.schemas.base import DatasetSchema, FieldDefinition

APPROVAL_SCHEMA = DatasetSchema(
    schema_id="approval-v2",
    generator_name="approval",
    version="2.0.0",
    description=(
        "Approval generator: one record = one subject decision "
        "(ApprovalRequest/ApprovalResponse grain) with bounded evidence"
    ),
    top_level_fields=(
        FieldDefinition(name="review_id", field_type=str, required=True),
        FieldDefinition(name="decision", field_type=dict, required=True),
        FieldDefinition(name="findings", field_type=list, required=True),
        FieldDefinition(name="evidence", field_type=list, required=True),
        FieldDefinition(name="recommendations", field_type=list, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
        FieldDefinition(name="record_id", field_type=str, required=True),
        FieldDefinition(name="capability", field_type=str, required=True),
        FieldDefinition(name="subject_id", field_type=str, required=True),
        FieldDefinition(name="source_object_id", field_type=str, required=True),
        FieldDefinition(name="subject", field_type=str, required=True),
        FieldDefinition(name="payload", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_version", "schema_version"),
)
