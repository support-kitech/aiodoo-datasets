"""Analysis validation."""

from aiodoo_datasets.generators.execution.analysis.context import AnalysisContext

class AnalysisValidator:
    """Validates AnalysisContext input hygiene before executing analyzers."""
    
    @classmethod
    def validate(cls, context: AnalysisContext) -> None:
        """Asserts context rules."""
        if not context.module:
            raise ValueError("AnalysisContext missing OdooModule")
        if not context.python_knowledge and not context.xml_knowledge:
            raise ValueError("AnalysisContext missing structural knowledge inputs")
