"""Protocol Mapper for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.domain.evaluation import Evaluation
from aiodoo_datasets.generators.evaluation.domain.benchmark_catalog import BenchmarkCatalog
from aiodoo_datasets.generators.evaluation.domain.benchmark_suite import BenchmarkSuite
from aiodoo_datasets.generators.evaluation.domain.evaluation_case import EvaluationCase
from aiodoo_datasets.generators.evaluation.domain.expected_output import ExpectedOutput
from aiodoo_datasets.generators.evaluation.domain.ground_truth import GroundTruth
from aiodoo_datasets.generators.evaluation.domain.evaluation_rule import EvaluationRule
from aiodoo_datasets.generators.evaluation.domain.success_criteria import SuccessCriteria
from aiodoo_datasets.generators.evaluation.domain.failure_criteria import FailureCriteria
from aiodoo_datasets.generators.evaluation.domain.reference import Reference
from aiodoo_datasets.generators.evaluation.domain.attachment import EvaluationAttachment
from aiodoo_datasets.generators.evaluation.domain.score import EvaluationScore
from aiodoo_datasets.generators.evaluation.domain.metadata import EvaluationMetadata
from aiodoo_datasets.generators.evaluation.domain.benchmark_metadata import BenchmarkMetadata
from aiodoo_datasets.generators.evaluation.protocol.domain.evaluation_protocol import (
    MetadataProtocol, ExpectedOutputProtocol, GroundTruthProtocol, EvaluationRuleProtocol,
    SuccessCriteriaProtocol, FailureCriteriaProtocol, ReferenceProtocol, AttachmentProtocol,
    ScoreProtocol, EvaluationCaseProtocol
)
from aiodoo_datasets.generators.evaluation.protocol.domain.benchmark_protocol import (
    BenchmarkMetadataProtocol, BenchmarkSuiteProtocol, BenchmarkCatalogProtocol, EvaluationProtocol
)

class ProtocolMapper:
    """Deterministically maps internal domain models to serialization protocols."""
    
    @staticmethod
    def map_evaluation(evaluation: Evaluation) -> EvaluationProtocol:
        """Map root Evaluation aggregate to protocol."""
        return EvaluationProtocol(
            evaluation_id=evaluation.evaluation_id,
            metadata=ProtocolMapper._map_metadata(evaluation.metadata),
            catalog=ProtocolMapper._map_catalog(evaluation.catalog)
        )
        
    @staticmethod
    def _map_metadata(metadata: EvaluationMetadata) -> MetadataProtocol:
        return MetadataProtocol(
            generator_version=metadata.generator_version,
            protocol_version=metadata.protocol_version,
            schema_version=metadata.schema_version,
            source_module=metadata.source_module,
            odoo_version=metadata.odoo_version,
            odoo_edition=metadata.odoo_edition,
            evaluation_type=metadata.evaluation_type.value if hasattr(metadata.evaluation_type, 'value') else metadata.evaluation_type,
            difficulty=metadata.difficulty.value if hasattr(metadata.difficulty, 'value') else metadata.difficulty,
            complexity=metadata.complexity
        )
        
    @staticmethod
    def _map_catalog(catalog: BenchmarkCatalog) -> BenchmarkCatalogProtocol:
        return BenchmarkCatalogProtocol(
            catalog_id=catalog.catalog_id,
            catalog_name=catalog.catalog_name,
            metadata=ProtocolMapper._map_benchmark_metadata(catalog.metadata),
            suites=tuple(ProtocolMapper._map_suite(s) for s in catalog.suites)
        )
        
    @staticmethod
    def _map_benchmark_metadata(metadata: BenchmarkMetadata) -> BenchmarkMetadataProtocol:
        return BenchmarkMetadataProtocol(
            suite_version=metadata.suite_version,
            benchmark_version=metadata.benchmark_version,
            benchmark_name=metadata.benchmark_name,
            benchmark_category=metadata.benchmark_category.value if hasattr(metadata.benchmark_category, 'value') else metadata.benchmark_category,
            benchmark_description=metadata.benchmark_description,
            target_generator=metadata.target_generator,
            supported_odoo_versions=tuple(metadata.supported_odoo_versions),
            supported_protocols=tuple(metadata.supported_protocols)
        )
        
    @staticmethod
    def _map_suite(suite: BenchmarkSuite) -> BenchmarkSuiteProtocol:
        return BenchmarkSuiteProtocol(
            suite_id=suite.suite_id,
            suite_name=suite.suite_name,
            cases=tuple(ProtocolMapper._map_case(c) for c in suite.cases)
        )
        
    @staticmethod
    def _map_case(case: EvaluationCase) -> EvaluationCaseProtocol:
        return EvaluationCaseProtocol(
            case_id=case.case_id,
            prompt=case.prompt,
            metadata=ProtocolMapper._map_metadata(case.metadata),
            expected_output=ProtocolMapper._map_expected_output(case.expected_output),
            ground_truth=ProtocolMapper._map_ground_truth(case.ground_truth),
            rules=tuple(ProtocolMapper._map_rule(r) for r in case.rules),
            success_criteria=tuple(ProtocolMapper._map_success_criteria(sc) for sc in case.success_criteria),
            failure_criteria=tuple(ProtocolMapper._map_failure_criteria(fc) for fc in case.failure_criteria),
            references=tuple(ProtocolMapper._map_reference(ref) for ref in case.references),
            attachments=tuple(ProtocolMapper._map_attachment(att) for att in case.attachments),
            scores=tuple(ProtocolMapper._map_score(score) for score in case.scores)
        )
        
    @staticmethod
    def _map_expected_output(out: ExpectedOutput) -> ExpectedOutputProtocol:
        return ExpectedOutputProtocol(
            output_id=out.output_id,
            expected_value=out.expected_value,
            value_type=out.value_type,
            required_elements=tuple(out.required_elements)
        )
        
    @staticmethod
    def _map_ground_truth(truth: GroundTruth) -> GroundTruthProtocol:
        return GroundTruthProtocol(
            ground_truth_id=truth.ground_truth_id,
            exact_match_required=truth.exact_match_required,
            keywords=tuple(truth.keywords)
        )
        
    @staticmethod
    def _map_rule(rule: EvaluationRule) -> EvaluationRuleProtocol:
        return EvaluationRuleProtocol(
            rule_id=rule.rule_id,
            description=rule.description,
            rule_type=rule.rule_type,
            parameters=tuple(rule.parameters)
        )
        
    @staticmethod
    def _map_success_criteria(criteria: SuccessCriteria) -> SuccessCriteriaProtocol:
        return SuccessCriteriaProtocol(
            criteria_id=criteria.criteria_id,
            description=criteria.description,
            weight=criteria.weight
        )
        
    @staticmethod
    def _map_failure_criteria(criteria: FailureCriteria) -> FailureCriteriaProtocol:
        return FailureCriteriaProtocol(
            criteria_id=criteria.criteria_id,
            description=criteria.description,
            fatal=criteria.fatal
        )
        
    @staticmethod
    def _map_reference(ref: Reference) -> ReferenceProtocol:
        return ReferenceProtocol(
            source_generator=ref.source_generator,
            source_reference=ref.source_reference,
            description=ref.description
        )
        
    @staticmethod
    def _map_attachment(att: EvaluationAttachment) -> AttachmentProtocol:
        return AttachmentProtocol(
            attachment_id=att.attachment_id,
            attachment_type=att.attachment_type.value if hasattr(att.attachment_type, 'value') else att.attachment_type,
            content=att.content,
            file_path=att.file_path
        )
        
    @staticmethod
    def _map_score(score: EvaluationScore) -> ScoreProtocol:
        return ScoreProtocol(
            score_id=score.score_id,
            metric_name=score.metric_name,
            raw_score=score.raw_score,
            max_score=score.max_score,
            normalized_score=score.normalized_score,
            weight=score.weight,
            pass_threshold=score.pass_threshold,
            result=score.result
        )
