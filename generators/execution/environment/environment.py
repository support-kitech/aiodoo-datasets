"""Execution environment context."""

from dataclasses import dataclass, field
from aiodoo_datasets.generators.execution.environment.edition import OdooEdition
from aiodoo_datasets.generators.execution.environment.version import OdooVersion
from aiodoo_datasets.generators.execution.environment.dependencies import (
    PythonDependency,
    SystemDependency,
    DatabaseDependency,
)


@dataclass(frozen=True, eq=True)
class ExecutionEnvironment:
    """
    Contextual execution limits and deployment constraints.

    Attributes:
        version: Target Odoo version.
        edition: Target Odoo edition.
        python_dependencies: Required external pip packages.
        system_dependencies: Required OS-level dependencies.
        database_dependencies: Required database extensions.
    """

    version: OdooVersion
    edition: OdooEdition
    python_dependencies: tuple[PythonDependency, ...] = field(default_factory=tuple)
    system_dependencies: tuple[SystemDependency, ...] = field(default_factory=tuple)
    database_dependencies: tuple[DatabaseDependency, ...] = field(default_factory=tuple)
