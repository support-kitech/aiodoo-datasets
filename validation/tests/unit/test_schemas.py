"""Unit tests for the Schema Framework."""

import unittest

from validation.exceptions import ValidationError
from validation.schemas.base import DatasetSchema, FieldDefinition
from validation.schemas.registry import SchemaRegistry
from validation.builders.schema_builder import SchemaBuilder


class TestFieldDefinition(unittest.TestCase):
    def test_immutable(self) -> None:
        fd = FieldDefinition(name="x", field_type=str, required=True)
        with self.assertRaises(AttributeError):
            fd.name = "y"  # type: ignore[misc]

    def test_defaults(self) -> None:
        fd = FieldDefinition(name="x")
        self.assertEqual(fd.field_type, object)
        self.assertTrue(fd.required)


class TestDatasetSchema(unittest.TestCase):
    def test_immutable(self) -> None:
        schema = DatasetSchema(schema_id="test-v1", generator_name="test")
        with self.assertRaises(AttributeError):
            schema.schema_id = "changed"  # type: ignore[misc]

    def test_required_field_names(self) -> None:
        schema = DatasetSchema(
            schema_id="test-v1",
            generator_name="test",
            top_level_fields=(
                FieldDefinition(name="a", required=True),
                FieldDefinition(name="b", required=False),
                FieldDefinition(name="c", required=True),
            ),
        )
        self.assertEqual(schema.required_field_names, frozenset({"a", "c"}))
        self.assertEqual(schema.optional_field_names, frozenset({"b"}))
        self.assertEqual(schema.all_field_names, frozenset({"a", "b", "c"}))

    def test_get_field(self) -> None:
        fd = FieldDefinition(name="x", field_type=str)
        schema = DatasetSchema(
            schema_id="test-v1",
            generator_name="test",
            top_level_fields=(fd,),
        )
        self.assertEqual(schema.get_field("x"), fd)
        self.assertIsNone(schema.get_field("missing"))


class TestSchemaRegistry(unittest.TestCase):
    def test_register_and_freeze(self) -> None:
        reg = SchemaRegistry()
        reg.register(DatasetSchema(schema_id="a", generator_name="gen_a"))
        reg.register(DatasetSchema(schema_id="b", generator_name="gen_b"))
        reg.freeze()
        self.assertTrue(reg.is_frozen)
        self.assertEqual(len(reg.all_schemas), 2)

    def test_duplicate_raises(self) -> None:
        reg = SchemaRegistry()
        reg.register(DatasetSchema(schema_id="a", generator_name="same"))
        with self.assertRaises(ValidationError):
            reg.register(DatasetSchema(schema_id="b", generator_name="same"))

    def test_frozen_mutation_raises(self) -> None:
        reg = SchemaRegistry()
        reg.freeze()
        with self.assertRaises(ValidationError):
            reg.register(DatasetSchema(schema_id="a", generator_name="x"))

    def test_get(self) -> None:
        reg = SchemaRegistry()
        schema = DatasetSchema(schema_id="a", generator_name="planner")
        reg.register(schema)
        reg.freeze()
        self.assertEqual(reg.get("planner"), schema)
        self.assertIsNone(reg.get("unknown"))

    def test_resolve_from_filename(self) -> None:
        reg = SchemaRegistry()
        schema = DatasetSchema(schema_id="a", generator_name="coding")
        reg.register(schema)
        reg.freeze()
        self.assertEqual(reg.resolve_from_filename("coding_v1_0.jsonl"), schema)
        self.assertIsNone(reg.resolve_from_filename("unknown.jsonl"))

    def test_hash_deterministic(self) -> None:
        reg1 = SchemaRegistry()
        reg1.register(DatasetSchema(schema_id="a", generator_name="x"))
        reg1.register(DatasetSchema(schema_id="b", generator_name="y"))
        reg1.freeze()

        reg2 = SchemaRegistry()
        reg2.register(DatasetSchema(schema_id="a", generator_name="x"))
        reg2.register(DatasetSchema(schema_id="b", generator_name="y"))
        reg2.freeze()

        self.assertEqual(reg1.hash_value, reg2.hash_value)

    def test_infer_generator(self) -> None:
        self.assertEqual(SchemaRegistry._infer_generator("planner_v1_0.jsonl"), "planner")
        self.assertEqual(SchemaRegistry._infer_generator("coding_v1_0.jsonl"), "coding")
        self.assertEqual(SchemaRegistry._infer_generator("context_v1_0.jsonl"), "context")
        self.assertEqual(SchemaRegistry._infer_generator("approval_dataset.jsonl"), "approval")
        self.assertEqual(SchemaRegistry._infer_generator("evaluation_dataset.jsonl"), "evaluation")
        self.assertEqual(SchemaRegistry._infer_generator("random.jsonl"), "unknown")


class TestSchemaBuilder(unittest.TestCase):
    def test_build_default(self) -> None:
        reg = SchemaBuilder.build_default()
        self.assertTrue(reg.is_frozen)
        self.assertEqual(len(reg.all_schemas), 8)

    def test_all_generators_registered(self) -> None:
        reg = SchemaBuilder.build_default()
        expected = {
            "planner",
            "coding",
            "repair",
            "context",
            "execution",
            "approval",
            "conversation",
            "evaluation",
        }
        actual = {s.generator_name for s in reg.all_schemas}
        self.assertEqual(actual, expected)

    def test_planner_schema(self) -> None:
        reg = SchemaBuilder.build_default()
        s = reg.get("planner")
        self.assertIsNotNone(s)
        self.assertIn("instruction", s.required_field_names)
        self.assertIn("output", s.required_field_names)
        self.assertIn("metadata", s.required_field_names)

    def test_context_schema(self) -> None:
        reg = SchemaBuilder.build_default()
        s = reg.get("context")
        self.assertIsNotNone(s)
        self.assertIn("id", s.required_field_names)
        self.assertIn("query", s.required_field_names)
        self.assertIn("artifacts", s.required_field_names)
        self.assertNotIn("instruction", s.required_field_names)

    def test_approval_schema(self) -> None:
        reg = SchemaBuilder.build_default()
        s = reg.get("approval")
        self.assertIsNotNone(s)
        self.assertIn("review_id", s.required_field_names)
        self.assertIn("decision", s.required_field_names)
        self.assertNotIn("instruction", s.required_field_names)

    def test_evaluation_schema(self) -> None:
        reg = SchemaBuilder.build_default()
        s = reg.get("evaluation")
        self.assertIsNotNone(s)
        self.assertIn("evaluation_id", s.required_field_names)
        self.assertIn("catalog", s.required_field_names)
        self.assertNotIn("instruction", s.required_field_names)


if __name__ == "__main__":
    unittest.main()
