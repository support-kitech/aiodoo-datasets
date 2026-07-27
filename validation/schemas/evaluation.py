"""Schema definition for the Evaluation capability SFT dataset."""

from validation.schemas.base import DatasetSchema, FieldDefinition

EVALUATION_SCHEMA = DatasetSchema(
    schema_id="evaluation-v2",
    generator_name="evaluation",
    version="2.0.0",
    description=(
        "Evaluation capability SFT: one record = one judgment "
        "(EvaluationRequest/EvaluationResponse grain)"
    ),
    top_level_fields=(
        FieldDefinition(name="record_id", field_type=str, required=True),
        FieldDefinition(name="candidate_id", field_type=str, required=True),
        FieldDefinition(name="evaluation_case_key", field_type=str, required=True),
        FieldDefinition(name="capability_under_test", field_type=str, required=True),
        FieldDefinition(name="candidate", field_type=dict, required=True),
        FieldDefinition(name="expectation", field_type=(dict, type(None)), required=False),
        FieldDefinition(name="rubric", field_type=str, required=False),
        FieldDefinition(name="verdict", field_type=str, required=True),
        FieldDefinition(name="score", field_type=(float, int, type(None)), required=False),
        FieldDefinition(name="explanation", field_type=str, required=False),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_version", "schema_version"),
)
