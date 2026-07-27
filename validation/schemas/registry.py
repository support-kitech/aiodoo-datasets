"""Freezable schema registry for generator-aware validation."""

import hashlib

from validation.exceptions import ValidationError
from validation.schemas.base import DatasetSchema

# Logical generator id for contract-shaped ``*_eval_corpus.jsonl`` files.
# Must be resolved *before* capability substrings such as ``coding`` /
# ``planner``, otherwise ``coding_eval_corpus.jsonl`` is misclassified as a
# training coding dataset.
EVAL_CORPUS_GENERATOR = "eval_corpus"


def infer_generator_from_filename(filename: str) -> str:
    """Infer the logical generator / corpus kind from a dataset filename."""
    name = filename.lower()
    if "eval_corpus" in name:
        return EVAL_CORPUS_GENERATOR
    for gen in (
        "planner",
        "coding",
        "repair",
        "context",
        "execution",
        "approval",
        "conversation",
        "evaluation",
    ):
        if gen in name:
            return gen
    return "unknown"


class SchemaRegistry:
    """
    A freezable registry of dataset schemas.

    Lifecycle: Create → Register → Freeze → Lookup Only

    Supports O(1) lookup by generator name.
    After freeze(), any mutation raises ValidationError.
    """

    def __init__(self) -> None:
        self._schemas: dict[str, DatasetSchema] = {}
        self._frozen: bool = False

    def _assert_mutable(self) -> None:
        if self._frozen:
            raise ValidationError("Cannot mutate a frozen SchemaRegistry.")

    def register(self, schema: DatasetSchema) -> None:
        """Register a schema. Raises on duplicate generator_name."""
        self._assert_mutable()
        if schema.generator_name in self._schemas:
            raise ValidationError(
                f"Duplicate schema registration for generator: {schema.generator_name}"
            )
        self._schemas[schema.generator_name] = schema

    def register_many(self, *schemas: DatasetSchema) -> None:
        """Register multiple schemas at once."""
        for schema in schemas:
            self.register(schema)

    def freeze(self) -> None:
        """Lock the registry."""
        self._assert_mutable()
        self._frozen = True

    @property
    def is_frozen(self) -> bool:
        return self._frozen

    def get(self, generator_name: str) -> DatasetSchema | None:
        """O(1) lookup by generator name."""
        return self._schemas.get(generator_name)

    def resolve_from_filename(self, filename: str) -> DatasetSchema | None:
        """Resolve the schema from a dataset filename."""
        generator = infer_generator_from_filename(filename)
        return self._schemas.get(generator)

    @property
    def all_schemas(self) -> tuple[DatasetSchema, ...]:
        """Return all registered schemas."""
        return tuple(self._schemas.values())

    @property
    def hash_value(self) -> str:
        """Deterministic SHA-256 hash of all registered schemas."""
        sha256 = hashlib.sha256()
        for name in sorted(self._schemas.keys()):
            schema = self._schemas[name]
            sha256.update(f"{schema.schema_id}:{schema.version}".encode("utf-8"))
            sha256.update(b"\x00")
        return sha256.hexdigest()

    @staticmethod
    def _infer_generator(filename: str) -> str:
        """Infer the generator name from a dataset filename."""
        return infer_generator_from_filename(filename)
