"""Pipeline orchestrator for the Approval Generator."""

from aiodoo_datasets.generators.approval.pipeline_context import PipelineContext
from aiodoo_datasets.generators.approval.pipeline_result import PipelineResult
from aiodoo_datasets.generators.approval.analysis.context import AnalysisContext
from aiodoo_datasets.generators.approval.analysis.analyzer import ApprovalAnalyzer
from aiodoo_datasets.generators.approval.engine.engine_context import EngineContext
from aiodoo_datasets.generators.approval.engine.decision_engine import DecisionEngine
from aiodoo_datasets.generators.approval.domain.review import Review
from aiodoo_datasets.generators.approval.protocol.mapper import ProtocolMapper
from aiodoo_datasets.generators.approval.validation.approval_validator import ApprovalValidator
from aiodoo_datasets.generators.approval.statistics.approval_statistics import ApprovalStatistics
from aiodoo_datasets.generators.common.export.writer import DatasetWriter
from aiodoo_datasets.generators.common.statistics.base_statistics import BaseStatistics
from aiodoo_datasets.generators.approval.exceptions import ApprovalPipelineError
import hashlib

class ApprovalExportStatistics(BaseStatistics):
    """Adapter for BaseStatistics to use in DatasetWriter."""
    def __init__(self, stats_dict):
        super().__init__()
        self.stats_dict = stats_dict
        
    def add_sample(self, record, json_str):
        pass # Handle natively inside BaseStatistics if we want, or do nothing
        
    def get_export_stats(self):
        return dict(self.stats_dict)

class ApprovalPipeline:
    """Orchestrates the entire Approval generation process."""
    
    @staticmethod
    def generate(context: PipelineContext) -> PipelineResult:
        """Execute the pipeline from inputs to final protocol."""
        diagnostics = []
        
        try:
            # 1. Analysis & Evidence Collection
            analysis_context = AnalysisContext(
                input_protocols=context.input_protocols,
            )
            analysis_result = ApprovalAnalyzer.analyze(analysis_context)
            
            # 2. Rule Evaluation & Decision Engine
            engine_context = EngineContext(
                metadata=context.metadata,
                evidence_pool=analysis_result.evidence_pool,
            )
            engine_result = DecisionEngine.execute(engine_context, context.rule_set)
            
            # 3. Assemble Review
            # Generate deterministic review ID based on input metadata signature
            hash_base = f"{context.metadata.source_module}:{context.metadata.generator_version}"
            review_hash = hashlib.sha256(hash_base.encode('utf-8')).hexdigest()[:8]
            
            review = Review(
                review_id=f"REV-{review_hash}",
                metadata=context.metadata,
                decision=engine_result.decision,
                findings=engine_result.findings,
                recommendations=engine_result.recommendations,
                evidence=analysis_result.evidence_pool,
            )
            
            # 4. Protocol Mapping
            protocol = ProtocolMapper.map_review(review)
            
            # 5. Validation
            validation_diags = ApprovalValidator.validate_all(review, protocol)
            diagnostics.extend(validation_diags)
            
            # 6. Statistics
            statistics = ApprovalStatistics.compile(review, context.rule_set, analysis_result.evidence_pool)
            
            # 7. Export
            export_stats = ApprovalExportStatistics(statistics)
            from pathlib import Path
            output_path = Path(context.config.output_dir)
            writer = DatasetWriter(
                output_dir=output_path,
                stats=export_stats,
                filename="approval_dataset.jsonl",
                dataset_name="approval"
            )
            writer.write_record(protocol)
            writer.export_manifest()
            writer.export_statistics()
            
            exported_files = [
                str(output_path / "approval_dataset.jsonl"),
                str(output_path / "dataset_manifest.json"),
                str(output_path / "statistics.json")
            ]
            
            return PipelineResult(
                success=True,
                approval_protocol=protocol,
                statistics=statistics,
                diagnostics=tuple(diagnostics),
                exported_files=tuple(exported_files)
            )
            
        except Exception as e:
            raise ApprovalPipelineError(f"Pipeline execution failed: {str(e)}") from e
