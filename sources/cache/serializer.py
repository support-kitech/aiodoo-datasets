"""Serializes the RepositoryContext into JSON format."""

import json
from pathlib import Path
from typing import Any

from sources.domain.context import RepositoryContext


class RepositoryEncoder(json.JSONEncoder):
    """Encodes immutable domain objects into JSON."""

    def default(self, o: Any) -> Any:
        if isinstance(o, Path):
            return str(o.resolve())
        if hasattr(o, "value") and isinstance(getattr(type(o), o.name, None), type(o)):
            # Handle Enums (RepositoryType, OdooVersion)
            return o.value
        if hasattr(o, "__dataclass_fields__"):
            # Handle Dataclasses (Repository, OdooModule, etc.)
            return {f: getattr(o, f) for f in o.__dataclass_fields__}
        return super().default(o)


class RepositorySerializer:
    """Handles serialization of RepositoryContext into persistent strings."""

    @staticmethod
    def serialize_context_repositories(context: RepositoryContext) -> list[tuple[str, str]]:
        """
        Serialize all repositories in the context.

        Args:
            context: The full RepositoryContext.

        Returns:
            A list of tuples (repository_name, json_string).
        """
        results = []
        for repo in context.repositories:
            repo_json = json.dumps(repo, cls=RepositoryEncoder)
            results.append((repo.name, repo_json))
        return results
