"""Schema definition for the Repair generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

REPAIR_SCHEMA = DatasetSchema(
    schema_id="repair-v1",
    generator_name="repair",
    version="1.0.0",
    description="Repair generator: instruction/context/output(RepairPayload)/metadata",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="context", field_type=dict, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
