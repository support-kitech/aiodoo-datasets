"""Execution environment representation."""

from aiodoo_datasets.generators.execution.environment.edition import OdooEdition
from aiodoo_datasets.generators.execution.environment.version import OdooVersion
from aiodoo_datasets.generators.execution.environment.environment import ExecutionEnvironment
from aiodoo_datasets.generators.execution.environment.dependencies import PythonDependency, SystemDependency, DatabaseDependency

__all__ = [
    "OdooEdition",
    "OdooVersion",
    "ExecutionEnvironment",
    "PythonDependency",
    "SystemDependency",
    "DatabaseDependency",
]
