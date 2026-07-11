"""After export hook."""

from aiodoo_datasets.generators.execution.export.export_context import ExportContext


class AfterExportHook:
    """Hook executed after export completes. Reserved for future integrations."""

    @staticmethod
    def execute(context: ExportContext) -> None:
        """Execute after export logic."""
        pass
