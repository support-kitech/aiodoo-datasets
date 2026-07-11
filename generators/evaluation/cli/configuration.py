"""CLI Configuration for Evaluation Generator."""

import yaml
from typing import Dict, Any


class Configuration:
    """Loads and validates CLI configuration."""

    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        """Load configuration from a YAML file."""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if data is not None else {}
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {config_path}: {e}")
