"""Before export hook."""

from aiodoo_datasets.generators.execution.export.export_context import ExportContext

class BeforeExportHook:
    """Hook executed before export begins. Reserved for future integrations."""
    
    @staticmethod
    def execute(context: ExportContext) -> None:
        """Execute before export logic."""
        pass
