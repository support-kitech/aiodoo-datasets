from aiodoo_datasets.generators.execution.builders.pipeline_result import PipelineResult

class BuilderValidator:
    """Orchestrates validation over the output of individual builders."""
    
    @classmethod
    def validate(cls, result: PipelineResult) -> None:
        """Validates all aggregated build results in the pipeline."""
        pass
