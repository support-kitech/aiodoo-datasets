"""Manages persistent state for resuming interrupted dataset generation pipelines."""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class CheckpointManager:
    """Handles JSON checkpointing to safely resume long-running pipeline processing."""

    def __init__(self, output_dir: Path, filename: str = "checkpoint.json") -> None:
        self.checkpoint_file = output_dir / filename
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)
        self.state: dict[str, Any] = {
            "processed_items": {},  # nested dict: repo -> module -> scenario -> list of hashes
            "processed_count": 0,
            "written_dataset_rows": 0,
            "timestamp": "",
        }

    def load(self) -> dict[str, Any]:
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    raw_state = json.load(f)

                    # Handle legacy flat structure "processed_modules" array
                    if "processed_modules" in raw_state:
                        flat_modules = raw_state.get("processed_modules", [])
                        items = {}  # type: ignore[var-annotated]
                        for m in flat_modules:
                            items.setdefault("legacy_repo", {})[m] = {"default": ["legacy_hash"]}
                        self.state["processed_items"] = items
                    else:
                        self.state["processed_items"] = raw_state.get("processed_items", {})

                    self.state["processed_count"] = raw_state.get("processed_count", 0)
                    self.state["written_dataset_rows"] = raw_state.get("written_dataset_rows", 0)
                    self.state["timestamp"] = raw_state.get("timestamp", "")

                    logger.info("Loaded nested checkpoint state.")
            except Exception as e:
                logger.error("Failed to load checkpoint, resetting state: %s", e)
                self.clear()
        else:
            self.state["processed_items"] = {}

        return self.state

    def save(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        """
        Accepts either:
        Flat (Planner): save(module_name: str, written_rows: int)
        Hierarchical (Coding): save(repo: str, module_name: str, scenario_name: str, protocol_hash: str, written_rows: int)
        """
        if len(args) == 2:
            repo = "legacy_repo"
            module_name = args[0]
            scenario_name = "default"
            protocol_hash = "legacy_hash"
            written_rows = args[1]
        elif len(args) == 5:
            repo, module_name, scenario_name, protocol_hash, written_rows = args
        else:
            return

        if not isinstance(self.state["processed_items"], dict):
            self.state["processed_items"] = {}

        items = self.state["processed_items"]
        if repo not in items:
            items[repo] = {}
        if module_name not in items[repo]:
            items[repo][module_name] = {}
        if scenario_name not in items[repo][module_name]:
            items[repo][module_name][scenario_name] = []

        if protocol_hash not in items[repo][module_name][scenario_name]:
            items[repo][module_name][scenario_name].append(protocol_hash)
            self.state["processed_count"] += 1

        self.state["written_dataset_rows"] = written_rows
        self.state["timestamp"] = datetime.utcnow().isoformat()

        temp_file = self.checkpoint_file.with_suffix(".json.tmp")
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=4)
            temp_file.replace(self.checkpoint_file)
        except Exception as e:
            logger.error("Failed to save checkpoint: %s", e)
            if temp_file.exists():
                temp_file.unlink()

    def clear(self) -> None:
        self.state = {
            "processed_items": {},
            "processed_count": 0,
            "written_dataset_rows": 0,
            "timestamp": "",
        }
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()

    def is_processed(self, *args) -> bool:  # type: ignore[no-untyped-def]
        """
        Accepts:
        Flat (Planner): is_processed(module_name: str)
        Hierarchical (Coding): is_processed(repo: str, module_name: str, scenario_name: str, protocol_hash: str)
        """
        items = self.state.get("processed_items", {})
        if not isinstance(items, dict):
            return False

        if len(args) == 1:
            module_name = args[0]
            for repo, modules in items.items():
                if module_name in modules:
                    return True
            return False
        elif len(args) == 4:
            repo, module_name, scenario_name, protocol_hash = args
            try:
                return protocol_hash in items.get(repo, {}).get(module_name, {}).get(
                    scenario_name, []
                )
            except AttributeError:
                return False
        return False

    def is_module_fully_processed(self, module_name: str) -> bool:
        """Helper to quickly check if a module is at least partially tracked (could be expanded to fully)."""
        items = self.state.get("processed_items", {})
        if not isinstance(items, dict):
            return False

        for repo, modules in items.items():
            if module_name in modules:
                return True
        return False
