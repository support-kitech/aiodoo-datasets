"""Base engineering artifact."""

from dataclasses import dataclass
from abc import ABC


@dataclass(frozen=True, eq=True)
class Artifact(ABC):
    """
    Base immutable representation of an engineering artifact.

    Attributes:
        module: The Odoo module owning the artifact (e.g., 'sale').
        relative_path: Path relative to the module root (e.g., 'models/sale.py').
        name: A specific logical name or identifier if applicable (e.g., 'sale.order').
    """

    module: str
    relative_path: str
    name: str
