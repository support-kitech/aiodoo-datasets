"""Registries for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.registries.parser_registry import ParserRegistry
from aiodoo_datasets.generators.evaluation.registries.factory_registry import FactoryRegistry
from aiodoo_datasets.generators.evaluation.registries.builder_registry import BuilderRegistry
from aiodoo_datasets.generators.evaluation.registries.validator_registry import ValidatorRegistry
from aiodoo_datasets.generators.evaluation.registries.benchmark_registry import BenchmarkRegistry

__all__ = [
    "ParserRegistry",
    "FactoryRegistry",
    "BuilderRegistry",
    "ValidatorRegistry",
    "BenchmarkRegistry",
]
