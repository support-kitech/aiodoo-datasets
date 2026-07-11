"""CLI for Evaluation Generator."""

from aiodoo_datasets.generators.evaluation.cli.arguments import get_parser
from aiodoo_datasets.generators.evaluation.cli.configuration import Configuration
from aiodoo_datasets.generators.evaluation.cli.commands import Commands
from aiodoo_datasets.generators.evaluation.cli.main import main

__all__ = [
    "get_parser",
    "Configuration",
    "Commands",
    "main",
]
