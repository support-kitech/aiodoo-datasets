"""SQLite-based cache store for the Sources Framework."""

import sqlite3
from pathlib import Path

from sources.domain.context import RepositoryContext
from sources.index.repository_index import RepositoryIndex
from sources.cache.cache_metadata import CacheMetadata
from sources.cache.serializer import RepositorySerializer
from sources.cache.deserializer import RepositoryDeserializer
from sources.exceptions import CacheError


class CacheStore:
    """Persists and loads RepositoryContext using SQLite."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize the SQLite schema."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS metadata (    key TEXT PRIMARY KEY,    value TEXT)"
                )
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS repositories ("
                    "    name TEXT PRIMARY KEY,"
                    "    data JSON"
                    ")"
                )
        except sqlite3.Error as e:
            raise CacheError(f"Failed to initialize cache DB: {e}")

    def clear(self) -> None:
        """Completely delete the cache file."""
        if self.db_path.exists():
            try:
                self.db_path.unlink()
            except OSError as e:
                raise CacheError(f"Failed to delete cache file: {e}")

    def save(self, context: RepositoryContext, metadata: CacheMetadata) -> None:
        """
        Persist the RepositoryContext to SQLite.

        Args:
            context: The fully built RepositoryContext.
            metadata: The CacheMetadata to save alongside it.

        Raises:
            CacheError: If serialization or database write fails.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Store Metadata
                meta_dict = {
                    "sources_framework_version": metadata.sources_framework_version,
                    "cache_schema_version": metadata.cache_schema_version,
                    "python_version": metadata.python_version,
                    "repository_count": metadata.repository_count,
                    "module_count": metadata.module_count,
                    "configuration_hash": metadata.configuration_hash,
                    "repository_hash": metadata.repository_hash,
                    "creation_time": metadata.creation_time,
                    "last_validation": metadata.last_validation,
                }
                for k, v in meta_dict.items():
                    conn.execute(
                        "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)", (k, str(v))
                    )

                # Store Repositories
                conn.execute("DELETE FROM repositories")
                serialized_repos = RepositorySerializer.serialize_context_repositories(context)
                for repo_name, repo_json in serialized_repos:
                    conn.execute(
                        "INSERT INTO repositories (name, data) VALUES (?, ?)",
                        (repo_name, repo_json),
                    )
        except (sqlite3.Error, TypeError) as e:
            raise CacheError(f"Failed to save cache: {e}")

    def load(self) -> tuple[RepositoryContext, CacheMetadata]:
        """
        Load the RepositoryContext and Metadata from SQLite.

        Returns:
            Tuple containing the restored RepositoryContext and CacheMetadata.

        Raises:
            CacheError: If the cache is missing, corrupted, or unreadable.
        """
        if not self.db_path.exists():
            raise CacheError("Cache database does not exist.")

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row

                # Load Metadata
                cur = conn.execute("SELECT key, value FROM metadata")
                meta_rows = cur.fetchall()
                if not meta_rows:
                    raise CacheError("Cache metadata is empty or corrupted.")

                meta_dict = {row["key"]: row["value"] for row in meta_rows}
                metadata = CacheMetadata(
                    sources_framework_version=meta_dict.get("sources_framework_version", ""),
                    cache_schema_version=meta_dict.get("cache_schema_version", ""),
                    python_version=meta_dict.get("python_version", ""),
                    repository_count=int(meta_dict.get("repository_count", 0)),
                    module_count=int(meta_dict.get("module_count", 0)),
                    configuration_hash=meta_dict.get("configuration_hash", ""),
                    repository_hash=meta_dict.get("repository_hash", ""),
                    creation_time=float(meta_dict.get("creation_time", 0.0)),
                    last_validation=float(meta_dict.get("last_validation", 0.0)),
                )

                # Load Repositories
                cur = conn.execute("SELECT name, data FROM repositories ORDER BY name")
                repo_rows = cur.fetchall()

                repositories = []
                for row in repo_rows:
                    json_str = row["data"]
                    repositories.append(RepositoryDeserializer.deserialize_repository(json_str))

        except (sqlite3.Error, KeyError, ValueError) as e:
            raise CacheError(f"Failed to load or parse cache: {e}")

        # Rebuild the Index and Context exactly as if scanned
        repo_tuple = tuple(repositories)
        index = RepositoryIndex(repo_tuple)

        context = RepositoryContext(
            repositories=repo_tuple,
            repository_index=index.repositories,
        )
        return context, metadata
