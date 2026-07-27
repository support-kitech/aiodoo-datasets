"""Schema definition for the Conversation generator dataset (next-reply grain)."""

from validation.schemas.base import DatasetSchema, FieldDefinition

CONVERSATION_SCHEMA = DatasetSchema(
    schema_id="conversation-v2",
    generator_name="conversation",
    version="2.0.0",
    description=(
        "Conversation generator: one record = one next-reply "
        "(ConversationRequest/ConversationResponse grain) with bounded history"
    ),
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
        FieldDefinition(name="context", field_type=dict, required=False),
        FieldDefinition(name="record_id", field_type=str, required=True),
        FieldDefinition(name="conversation_id", field_type=str, required=True),
        FieldDefinition(name="turn_index", field_type=int, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
