"""Knowledge validation."""

from aiodoo_datasets.generators.execution.analysis.knowledge.execution_knowledge import ExecutionKnowledge

class KnowledgeValidator:
    """Validates the extracted ExecutionKnowledge before passing to Builders."""
    
    @classmethod
    def validate(cls, knowledge: ExecutionKnowledge) -> None:
        """Asserts knowledge output rules."""
        if not knowledge.artifacts and not knowledge.operations:
            raise ValueError("ExecutionKnowledge is completely empty")
