"""Schema definition for contract-shaped evaluation corpus JSONL files.

``*_eval_corpus.jsonl`` records are produced by
:mod:`generators.common.contract.eval_corpus` and intentionally use the
canonical ``aiodoo_contract`` case shape
(``capability`` / ``request`` / ``expected_response`` / ``source_protocol_hash``),
not the per-generator training row envelope
(``instruction`` / ``context`` / ``output`` / ``metadata``).
"""

from validation.schemas.base import DatasetSchema, FieldDefinition

EVAL_CORPUS_SCHEMA = DatasetSchema(
    schema_id="eval-corpus-v1",
    generator_name="eval_corpus",
    version="1.0.0",
    description=(
        "Contract evaluation corpus: capability/request/expected_response/"
        "source_protocol_hash gold pairs for aiodoo-validation"
    ),
    top_level_fields=(
        FieldDefinition(name="capability", field_type=str, required=True),
        FieldDefinition(name="request", field_type=dict, required=True),
        FieldDefinition(name="expected_response", field_type=dict, required=True),
        FieldDefinition(
            name="source_protocol_hash",
            field_type=(str, type(None)),
            required=False,
            description="Optional back-reference to the source training record hash",
        ),
    ),
    metadata_required_fields=(),
)
