"""
Approval Generator Public API

Provides deterministic engineering review dataset generation.
"""

from generators.approval.version import __version__
from generators.approval.api import generate, validate, export

__all__ = ["__version__", "generate", "validate", "export"]
