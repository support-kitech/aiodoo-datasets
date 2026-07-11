"""Schema definition for the Conversation generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

CONVERSATION_SCHEMA = DatasetSchema(
    schema_id="conversation-v1",
    generator_name="conversation",
    version="1.0.0",
    description="Conversation generator: instruction/output/metadata (standard format)",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
        FieldDefinition(name="context", field_type=dict, required=False),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
