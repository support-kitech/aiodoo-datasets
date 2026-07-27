"""Builds the default SchemaRegistry with all generator schemas."""

from validation.schemas.registry import SchemaRegistry
from validation.schemas.planner import PLANNER_SCHEMA
from validation.schemas.coding import CODING_SCHEMA
from validation.schemas.repair import REPAIR_SCHEMA
from validation.schemas.context import CONTEXT_SCHEMA
from validation.schemas.execution import EXECUTION_SCHEMA
from validation.schemas.approval import APPROVAL_SCHEMA
from validation.schemas.conversation import CONVERSATION_SCHEMA
from validation.schemas.evaluation import EVALUATION_SCHEMA
from validation.schemas.eval_corpus import EVAL_CORPUS_SCHEMA


class SchemaBuilder:
    """Constructs the default SchemaRegistry with all generator schemas."""

    @staticmethod
    def build_default() -> SchemaRegistry:
        """Create a registry with all production schemas, frozen and ready."""
        registry = SchemaRegistry()
        registry.register_many(
            PLANNER_SCHEMA,
            CODING_SCHEMA,
            REPAIR_SCHEMA,
            CONTEXT_SCHEMA,
            EXECUTION_SCHEMA,
            APPROVAL_SCHEMA,
            CONVERSATION_SCHEMA,
            EVALUATION_SCHEMA,
            EVAL_CORPUS_SCHEMA,
        )
        registry.freeze()
        return registry
