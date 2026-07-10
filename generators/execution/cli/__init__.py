"""CLI package."""

from aiodoo_datasets.generators.execution.cli.arguments import parse_args
from aiodoo_datasets.generators.execution.cli.configuration import build_pipeline_context
from aiodoo_datasets.generators.execution.cli.commands import run_pipeline
from aiodoo_datasets.generators.execution.cli.main import main

__all__ = [
    "parse_args",
    "build_pipeline_context",
    "run_pipeline",
    "main",
]
