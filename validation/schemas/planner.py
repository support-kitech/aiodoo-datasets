"""Schema definition for the Planner generator dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

PLANNER_SCHEMA = DatasetSchema(
    schema_id="planner-v1",
    generator_name="planner",
    version="1.0.0",
    description="Planner generator: instruction/input/output(PlanPayload)/metadata",
    top_level_fields=(
        FieldDefinition(name="instruction", field_type=str, required=True),
        FieldDefinition(name="input", field_type=str, required=True),
        FieldDefinition(name="output", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_hash", "module"),
)
