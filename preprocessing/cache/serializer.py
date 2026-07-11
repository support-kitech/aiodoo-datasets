"""Serializer for preprocessing domain objects."""

import json

from preprocessing.domain.context import PreprocessedRepositoryContext


class Serializer:
    """Serializes a PreprocessedRepositoryContext to JSON."""

    @staticmethod
    def serialize(context: PreprocessedRepositoryContext) -> str:
        """Convert the full context graph to a JSON string."""

        repos = []
        for repo in context.repositories:
            modules = []
            for module in repo.modules:
                files = []
                for file_node in module.files:
                    files.append(
                        {
                            "file_path": file_node.file_path.as_posix(),
                            "normalized_path": file_node.normalized_path.as_posix(),
                            "language": file_node.language.value,
                            "raw_content": file_node.raw_content,
                            "normalized_content": file_node.normalized_content,
                            "duplicate_status": file_node.duplicate_status.value,
                            "metadata": dict(file_node.metadata),
                            "warnings": list(file_node.warnings),
                            "statistics": {
                                "whitespace_removed_bytes": file_node.statistics.whitespace_removed_bytes,
                                "comments_normalized": file_node.statistics.comments_normalized,
                                "tokens_estimated": file_node.statistics.tokens_estimated,
                                "duplicates_detected": file_node.statistics.duplicates_detected,
                            },
                        }
                    )

                modules.append(
                    {"name": module.name, "files": files, "metadata": dict(module.metadata)}
                )

            repos.append(
                {
                    "name": repo.name,
                    "odoo_version": repo.odoo_version.value,
                    "repository_type": repo.repository_type.value,
                    "modules": modules,
                    "metadata": dict(repo.metadata),
                }
            )

        data = {"repositories": repos, "metadata": dict(context.metadata)}

        return json.dumps(data)
