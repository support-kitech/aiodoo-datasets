"""CLI Configuration for Evaluation Generator."""

import json
from typing import Dict, Any

class Configuration:
    """Loads and validates CLI configuration."""
    
    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        """Load configuration from a JSON file."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {config_path}: {e}")
