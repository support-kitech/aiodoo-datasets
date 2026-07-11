"""SQLite Cache Store."""

import sqlite3
import json
from pathlib import Path

from preprocessing.cache.cache_key import CacheKey
from preprocessing.cache.cache_metadata import CacheMetadata
from preprocessing.exceptions import PreprocessingError


class CacheStore:
    """
    SQLite-backed cache store for serialized preprocessing payloads.
    Does NOT understand the domain objects, only stores JSON.
    """
    
    def __init__(self, db_path: Path):
        self._db_path = db_path
        self._init_db()
        
    def _init_db(self) -> None:
        """Initialize the SQLite schema if it doesn't exist."""
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self._db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS preprocessing_cache (
                    cache_key TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
    def get(self, key: CacheKey) -> tuple[str, CacheMetadata] | None:
        """Fetch a serialized payload and its metadata."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.execute(
                    "SELECT payload, metadata FROM preprocessing_cache WHERE cache_key = ?",
                    (key.value,)
                )
                row = cursor.fetchone()
                
                if row:
                    payload, meta_json = row
                    if isinstance(payload, bytes):
                        payload = __import__('zlib').decompress(payload).decode('utf-8')

                    meta_dict = json.loads(meta_json)
                    from types import MappingProxyType
                    metadata = CacheMetadata(
                        cache_key=meta_dict["cache_key"],
                        created_at_iso=meta_dict["created_at_iso"],
                        framework_version=meta_dict["framework_version"],
                        python_version=meta_dict.get("python_version", "unknown"),
                        cache_schema_version=meta_dict.get("cache_schema_version", "1.0"),
                        serializer_version=meta_dict.get("serializer_version", "1.0"),
                        repository_context_hash=meta_dict.get("repository_context_hash", ""),
                        preprocessed_context_hash=meta_dict.get("preprocessed_context_hash", ""),
                        processor_registry_hash=meta_dict.get("processor_registry_hash", ""),
                        statistics=MappingProxyType(meta_dict.get("statistics", {}))
                    )
                    return payload, metadata
                return None
        except sqlite3.Error as e:
            raise PreprocessingError(f"Cache read failed: {e}")

    def set(self, key: CacheKey, payload: str, metadata: CacheMetadata) -> None:
        """Persist a serialized payload."""
        meta_dict = {
            "cache_key": metadata.cache_key,
            "created_at_iso": metadata.created_at_iso,
            "framework_version": metadata.framework_version,
            "python_version": metadata.python_version,
            "cache_schema_version": metadata.cache_schema_version,
            "serializer_version": metadata.serializer_version,
            "repository_context_hash": metadata.repository_context_hash,
            "preprocessed_context_hash": metadata.preprocessed_context_hash,
            "processor_registry_hash": metadata.processor_registry_hash,
            "statistics": dict(metadata.statistics)
        }
        
        try:
            compressed_payload = __import__('zlib').compress(payload.encode('utf-8'))
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    "INSERT OR REPLACE INTO preprocessing_cache (cache_key, payload, metadata) VALUES (?, ?, ?)",
                    (key.value, compressed_payload, json.dumps(meta_dict))
                )
        except sqlite3.Error as e:
            raise PreprocessingError(f"Cache write failed: {e}")
            
    def clear(self) -> None:
        """Clear the entire cache."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute("DELETE FROM preprocessing_cache")
        except sqlite3.Error as e:
            raise PreprocessingError(f"Cache clear failed: {e}")
