"""Generates base metadata for AIODOO Dataset Generator rows."""

import datetime
from typing import Any

from preprocessing.domain.repository import PreprocessedModule
from generators.common.discovery.classifier import Scenario

_GIT_CACHE: dict[str, str] = {}


def get_git_commit(module: PreprocessedModule) -> str:
    """Retrieve and cache the git commit for the repository."""
    from pathlib import Path

    repo_path = str(Path(str(module.metadata["path"])).parent.absolute())
    if repo_path in _GIT_CACHE:
        return _GIT_CACHE[repo_path]

    import subprocess

    git_commit = None
    try:
        git_commit_output = (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=repo_path, stderr=subprocess.DEVNULL, timeout=2
            )
            .decode("utf-8")
            .strip()
        )
        if git_commit_output:
            git_commit = git_commit_output
    except (subprocess.SubprocessError, OSError, Exception):
        pass

    _GIT_CACHE[repo_path] = git_commit  # type: ignore[assignment]
    return git_commit  # type: ignore[return-value]


def compute_difficulty(metrics: dict[str, int]) -> int:
    """Calculate an engineering complexity score from 1 to 5."""
    if not metrics:
        return 1

    score = 0
    score += metrics.get("models", 0) * 2
    score += metrics.get("fields", 0) * 1
    score += metrics.get("views", 0) * 2
    score += metrics.get("controllers", 0) * 3
    # Planner specific additions
    score += metrics.get("reports", 0) * 2
    score += metrics.get("security_rules", 0) * 2
    score += metrics.get("scheduled_actions", 0) * 3
    score += metrics.get("dependencies", 0) * 1
    score += metrics.get("assets", 0) * 1
    score += metrics.get("file_count", 0) * 0.5  # type: ignore[assignment]

    if score < 10:
        return 1
    elif score < 30:
        return 2
    elif score < 60:
        return 3
    elif score < 100:
        return 4
    else:
        return 5


def build_base_metadata(module: PreprocessedModule, scenario: Scenario) -> dict[str, Any]:
    """Compile the base metadata dictionary for the JSONL row with full provenance."""
    difficulty = (
        compute_difficulty(scenario.metrics)
        if getattr(scenario, "metrics", None)
        else scenario.difficulty
    )

    from pathlib import Path

    module_path = Path(str(module.metadata["path"]))
    python_files = sorted(
        [str(f.normalized_path) for f in module.files if str(f.normalized_path).endswith(".py")]
    )
    xml_files = sorted(
        [str(f.normalized_path) for f in module.files if str(f.normalized_path).endswith(".xml")]
    )

    git_commit = get_git_commit(module)

    manifest_name = (
        "__manifest__.py" if (module_path / "__manifest__.py").exists() else "__openerp__.py"
    )
    manifest_path = str(module_path / manifest_name)

    file_count = len(module.files)

    return {
        "repository": f"odoo/{module.metadata.get('version', '')}",
        "repository_type": "git" if git_commit is not None else "archive",
        "repository_version": module.metadata.get("version", ""),
        "edition": "ce",
        "version": module.metadata.get("version", ""),
        "odoo_version": module.metadata.get("version", ""),
        "module": module.name,
        "module_path": str(module_path.absolute()),
        "manifest_path": manifest_path,
        "python_files": python_files,
        "xml_files": xml_files,
        "source_checksum": "",
        "source_file_count": file_count,
        "module_hash": "",
        "manifest_hash": "",
        "generator_version": "0.1.0",
        "protocol_version": "1.0",
        "generation_timestamp": datetime.datetime.utcnow().isoformat(),
        "git_commit": git_commit,
        "scenario": [scenario.name] + scenario.tags,
        "difficulty": difficulty,
        "engineering_metrics": getattr(scenario, "metrics", None),
    }
