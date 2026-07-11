"""Benchmark Protocol models for Evaluation Generator."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Tuple
from aiodoo_datasets.generators.evaluation.protocol.domain.evaluation_protocol import (
    EvaluationCaseProtocol,
    MetadataProtocol,
)


class BenchmarkMetadataProtocol(BaseModel):
    """Protocol for BenchmarkMetadata."""

    model_config = ConfigDict(frozen=True)
    suite_version: str
    benchmark_version: str
    benchmark_name: str
    benchmark_category: str
    benchmark_description: str
    target_generator: str
    supported_odoo_versions: Tuple[str, ...] = Field(default=())
    supported_protocols: Tuple[str, ...] = Field(default=())


class BenchmarkSuiteProtocol(BaseModel):
    """Protocol for BenchmarkSuite."""

    model_config = ConfigDict(frozen=True)
    suite_id: str
    suite_name: str
    cases: Tuple[EvaluationCaseProtocol, ...] = Field(default=())


class BenchmarkCatalogProtocol(BaseModel):
    """Protocol for BenchmarkCatalog."""

    model_config = ConfigDict(frozen=True)
    catalog_id: str
    catalog_name: str
    metadata: BenchmarkMetadataProtocol
    suites: Tuple[BenchmarkSuiteProtocol, ...] = Field(default=())


class EvaluationProtocol(BaseModel):
    """Root Protocol for Evaluation aggregate."""

    model_config = ConfigDict(frozen=True)
    evaluation_id: str
    metadata: MetadataProtocol
    catalog: BenchmarkCatalogProtocol
