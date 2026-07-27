"""Schema definition for the Evaluation BenchmarkCatalog side artifact."""

from validation.schemas.base import DatasetSchema, FieldDefinition

BENCHMARK_CATALOG_SCHEMA = DatasetSchema(
    schema_id="benchmark-catalog-v1",
    generator_name="benchmark_catalog",
    version="1.0.0",
    description=(
        "BenchmarkCatalog artifact for certification/benchmarking/regression — "
        "NOT Evaluation capability SFT"
    ),
    top_level_fields=(
        FieldDefinition(name="evaluation_id", field_type=str, required=True),
        FieldDefinition(name="catalog", field_type=dict, required=True),
        FieldDefinition(name="metadata", field_type=dict, required=True),
    ),
    metadata_required_fields=("protocol_version", "schema_version"),
)
