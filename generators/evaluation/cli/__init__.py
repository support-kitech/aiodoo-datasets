"""CLI for Evaluation Generator."""

from generators.evaluation.cli.arguments import get_parser
from generators.evaluation.cli.configuration import Configuration
from generators.evaluation.cli.commands import Commands
from generators.evaluation.cli.main import main

__all__ = [
    "get_parser",
    "Configuration",
    "Commands",
    "main",
]
