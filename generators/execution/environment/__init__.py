"""Execution environment representation."""

from generators.execution.environment.edition import OdooEdition
from generators.execution.environment.version import OdooVersion
from generators.execution.environment.environment import ExecutionEnvironment
from generators.execution.environment.dependencies import (
    PythonDependency,
    SystemDependency,
    DatabaseDependency,
)

__all__ = [
    "OdooEdition",
    "OdooVersion",
    "ExecutionEnvironment",
    "PythonDependency",
    "SystemDependency",
    "DatabaseDependency",
]
