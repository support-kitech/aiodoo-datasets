"""Repository builder."""

from sources.domain.repository import Repository
from preprocessing.domain.repository import PreprocessedRepository, PreprocessedModule
from preprocessing.domain.file import NormalizedFile


class RepositoryBuilder:
    """Builds an immutable PreprocessedRepository."""
    
    @staticmethod
    def build(source_repo: Repository, modules: tuple[PreprocessedModule, ...]) -> PreprocessedRepository:
        """
        Constructs the repository ensuring deterministic ordering of modules.
        """
        sorted_modules = tuple(sorted(modules, key=lambda m: m.name))
        
        return PreprocessedRepository(
            name=source_repo.name,
            odoo_version=source_repo.version,
            repository_type=source_repo.repository_type,
            modules=sorted_modules
        )

    @staticmethod
    def build_module(name: str, files: tuple[NormalizedFile, ...], metadata: dict[str, object] | None = None) -> PreprocessedModule:
        """Constructs a module ensuring deterministic ordering of files."""
        from types import MappingProxyType
        sorted_files = tuple(sorted(files, key=lambda f: f.normalized_path))
        
        return PreprocessedModule(
            name=name,
            files=sorted_files,
            metadata=MappingProxyType(metadata) if metadata else MappingProxyType({})
        )
