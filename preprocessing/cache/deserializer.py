"""Deserializer for preprocessing domain objects."""

import json
from pathlib import Path
from types import MappingProxyType

from sources.domain.enums import OdooVersion, RepositoryType
from preprocessing.domain.context import PreprocessedRepositoryContext
from preprocessing.domain.repository import PreprocessedRepository, PreprocessedModule
from preprocessing.domain.file import NormalizedFile, DuplicateStatus, Language
from preprocessing.domain.stats import TransformationStatistics


class Deserializer:
    """Deserializes JSON to a PreprocessedRepositoryContext."""

    @staticmethod
    def deserialize(payload: str) -> PreprocessedRepositoryContext:
        """Convert a JSON string to a full context graph."""
        data = json.loads(payload)

        repos = []
        for repo_data in data["repositories"]:
            modules = []
            for module_data in repo_data["modules"]:
                files = []
                for file_data in module_data["files"]:
                    stats_data = file_data["statistics"]
                    stats = TransformationStatistics(
                        whitespace_removed_bytes=stats_data.get("whitespace_removed_bytes", 0),
                        comments_normalized=stats_data.get("comments_normalized", 0),
                        tokens_estimated=stats_data.get("tokens_estimated", 0),
                        duplicates_detected=stats_data.get("duplicates_detected", 0),
                    )

                    file_node = NormalizedFile(
                        file_path=Path(file_data["file_path"]),
                        normalized_path=Path(file_data["normalized_path"]),
                        language=Language(file_data["language"]),
                        raw_content=file_data["raw_content"],
                        normalized_content=file_data["normalized_content"],
                        duplicate_status=DuplicateStatus(file_data["duplicate_status"]),
                        metadata=MappingProxyType(file_data.get("metadata", {})),
                        warnings=tuple(file_data.get("warnings", [])),
                        statistics=stats,
                    )
                    files.append(file_node)

                module = PreprocessedModule(
                    name=module_data["name"],
                    files=tuple(files),
                    metadata=MappingProxyType(module_data.get("metadata", {})),
                )
                modules.append(module)

            repo = PreprocessedRepository(
                name=repo_data["name"],
                odoo_version=OdooVersion(repo_data["odoo_version"]),
                repository_type=RepositoryType(repo_data["repository_type"]),
                modules=tuple(modules),
                metadata=MappingProxyType(repo_data.get("metadata", {})),
            )
            repos.append(repo)

        return PreprocessedRepositoryContext(
            repositories=tuple(repos), metadata=MappingProxyType(data.get("metadata", {}))
        )
