"""Fast, immutable lookup index for repositories and modules."""

from types import MappingProxyType

from sources.domain.enums import OdooVersion, RepositoryType
from sources.domain.repository import Repository
from sources.domain.module import OdooModule
from sources.exceptions import RepositoryError


class RepositoryIndex:
    """Immutable O(1) lookup index for the Sources Framework."""

    def __init__(self, repositories: tuple[Repository, ...]):
        """
        Initialize the index with fully built repositories.

        Args:
            repositories: Tuple of all loaded repositories.
        """
        self._repositories = repositories

        # Internal dictionaries for construction
        repo_by_name: dict[str, Repository] = {}
        repo_by_version: dict[OdooVersion, list[Repository]] = {}
        repo_by_type: dict[RepositoryType, list[Repository]] = {}
        module_by_name: dict[str, list[OdooModule]] = {}

        for repo in repositories:
            repo_by_name[repo.name] = repo
            
            if repo.version not in repo_by_version:
                repo_by_version[repo.version] = []
            repo_by_version[repo.version].append(repo)
            
            if repo.repository_type not in repo_by_type:
                repo_by_type[repo.repository_type] = []
            repo_by_type[repo.repository_type].append(repo)

            for module in repo.modules:
                if module.technical_name not in module_by_name:
                    module_by_name[module.technical_name] = []
                module_by_name[module.technical_name].append(module)

        # Freeze into MappingProxyTypes for internal use and properties
        self._repo_by_name: MappingProxyType[str, Repository] = MappingProxyType(repo_by_name)
        self._repo_by_version: MappingProxyType[OdooVersion, tuple[Repository, ...]] = MappingProxyType(
            {k: tuple(v) for k, v in repo_by_version.items()}
        )
        self._repo_by_type: MappingProxyType[RepositoryType, tuple[Repository, ...]] = MappingProxyType(
            {k: tuple(v) for k, v in repo_by_type.items()}
        )
        self._module_by_name: MappingProxyType[str, tuple[OdooModule, ...]] = MappingProxyType(
            {k: tuple(v) for k, v in module_by_name.items()}
        )

    @property
    def modules(self) -> MappingProxyType[str, tuple[OdooModule, ...]]:
        """Immutable view of modules indexed by technical name."""
        return self._module_by_name

    @property
    def repositories(self) -> MappingProxyType[str, Repository]:
        """Immutable view of repositories indexed by name."""
        return self._repo_by_name

    @property
    def versions(self) -> MappingProxyType[OdooVersion, tuple[Repository, ...]]:
        """Immutable view of repositories indexed by version."""
        return self._repo_by_version

    @property
    def repository_types(self) -> MappingProxyType[RepositoryType, tuple[Repository, ...]]:
        """Immutable view of repositories indexed by repository type."""
        return self._repo_by_type

    def find_repository(self, name: str) -> Repository:
        """Find a repository by its unique name."""
        try:
            return self._repo_by_name[name]
        except KeyError:
            raise RepositoryError(f"Repository not found: {name}")

    def find_by_version(self, version: OdooVersion) -> tuple[Repository, ...]:
        """Find all repositories matching a specific Odoo version."""
        return self._repo_by_version.get(version, tuple())

    def find_by_type(self, repo_type: RepositoryType) -> tuple[Repository, ...]:
        """Find all repositories matching a specific repository type."""
        return self._repo_by_type.get(repo_type, tuple())

    def find_module(self, technical_name: str) -> tuple[OdooModule, ...]:
        """
        Find all instances of a module by its technical name.
        """
        return self._module_by_name.get(technical_name, tuple())
