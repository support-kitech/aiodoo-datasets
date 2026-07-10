"""Environment dependency structures."""

from dataclasses import dataclass

@dataclass(frozen=True, eq=True)
class PythonDependency:
    """Represents a Python pip dependency."""
    name: str
    version_specifier: str | None = None

@dataclass(frozen=True, eq=True)
class SystemDependency:
    """Represents an OS-level dependency."""
    name: str
    package_manager: str | None = None

@dataclass(frozen=True, eq=True)
class DatabaseDependency:
    """Represents a database-level configuration or extension dependency."""
    name: str
    version_specifier: str | None = None
