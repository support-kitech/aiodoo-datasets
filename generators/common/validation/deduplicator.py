"""Prevents generating duplicate datasets across Odoo versions."""

import threading
import logging

logger = logging.getLogger(__name__)


class Deduplicator:
    """Thread-safe hash registry to prevent duplicate planner outputs based on deterministic Protocol Hashes."""

    def __init__(self) -> None:
        self._hashes = set()  # type: ignore[var-annotated]
        self._lock = threading.Lock()

    def is_unique(self, protocol_hash: str) -> bool:
        """Determines if the payload is unique strictly via its Protocol Hash."""
        with self._lock:
            if protocol_hash in self._hashes:
                return False
            self._hashes.add(protocol_hash)
            return True
