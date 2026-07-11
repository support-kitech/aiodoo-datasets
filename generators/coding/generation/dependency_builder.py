"""Determines implementation dependencies for topological sorting."""

from typing import Any
from dataclasses import dataclass

import re
import ast
from pathlib import Path
from preprocessing.domain.repository import PreprocessedModule


def _extract_python_deps(file_path: Path) -> set[str]:
    deps = set()
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id == "_inherit":
                            if isinstance(node.value, ast.Constant):
                                deps.add(str(node.value.value))
                            elif isinstance(node.value, ast.List):
                                for elt in node.value.elts:
                                    if isinstance(elt, ast.Constant):
                                        deps.add(str(elt.value))
                        elif target.id == "_inherits" and isinstance(node.value, ast.Dict):
                            for key in node.value.keys:
                                if isinstance(key, ast.Constant):
                                    deps.add(str(key.value))
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr in (
                    "Many2one",
                    "One2many",
                    "Many2many",
                ):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        deps.add(str(node.args[0].value))
                    else:
                        for kw in node.keywords:
                            if kw.arg in ("comodel_name", "relation") and isinstance(
                                kw.value, ast.Constant
                            ):
                                deps.add(str(kw.value.value))
    except Exception:
        pass
    return deps


def _extract_xml_deps(file_path: Path) -> set[str]:
    deps = set()
    try:
        content = file_path.read_text(encoding="utf-8")
        # Extract inherit_id
        for match in re.finditer(r'<field name="inherit_id" ref="([^"]+)"', content):
            deps.add(match.group(1))
        # Extract model references
        for match in re.finditer(r'model="([^"]+)"', content):
            deps.add(match.group(1))
    except Exception:
        pass
    return deps


@dataclass
class DependencyNode:
    id: str
    path: str


@dataclass
class DependencyEdge:
    source_id: str
    target_id: str
    reason: str


class DependencyGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, DependencyNode] = {}
        self.edges: list[DependencyEdge] = []

    def add_node(self, node_id: str, path: str):  # type: ignore[no-untyped-def]
        if node_id not in self.nodes:
            self.nodes[node_id] = DependencyNode(id=node_id, path=path)

    def add_edge(self, source_id: str, target_id: str, reason: str):  # type: ignore[no-untyped-def]
        self.edges.append(DependencyEdge(source_id=source_id, target_id=target_id, reason=reason))

    def get_dependencies_for(self, source_id: str) -> list[str]:
        return list(set([edge.target_id for edge in self.edges if edge.source_id == source_id]))


def determine_dependencies(
    artifact_path: str,
    all_artifacts: list[dict[str, Any]],
    py_k: Any,
    xml_k: Any,
    module: PreprocessedModule,
) -> list[str]:
    """
    Builds a semantic dependency graph based on actual engineering relationships.
    Internally constructs a typed DependencyGraph before flattening for the protocol schema.
    """
    graph = DependencyGraph()
    abs_path = Path(str(module.metadata["path"])) / artifact_path

    # We need a stable ID generation mechanism here since artifact_builder hasn't mapped them yet.
    # Fortunately, the artifact_mapper uses a deterministic hash based on module_version, module_name, and path.
    import hashlib

    def get_id(path: str) -> str:
        seed = f"{module.metadata.get('version', '')}_{module.name}_file_{path}"
        return f"art_{hashlib.sha256(seed.encode('utf-8')).hexdigest()[:12]}"

    current_id = get_id(artifact_path)
    graph.add_node(current_id, artifact_path)

    for a in all_artifacts:
        a_id = get_id(a["path"])
        graph.add_node(a_id, a["path"])

    if not abs_path.exists():
        return []

    path_lower = artifact_path.lower()
    semantic_refs = set()

    if path_lower.endswith(".py"):
        semantic_refs = _extract_python_deps(abs_path)
    elif path_lower.endswith(".xml") or "security/" in path_lower:
        semantic_refs = _extract_xml_deps(abs_path)

    # Build Edges
    for a in all_artifacts:
        a_path = a["path"]
        if a_path == artifact_path:
            continue

        a_id = get_id(a_path)
        a_path_lower = a_path.lower()

        # Manifest is the root dependency for structural reasons
        if "__manifest__.py" in a_path_lower or "__openerp__.py" in a_path_lower:
            graph.add_edge(
                current_id, a_id, "Structural requirement: Manifest is always loaded first."
            )

        if path_lower.endswith(".xml") and "models/" in a_path_lower:
            # Views depend on models. If semantic_refs has models, depend on python files.
            if len(semantic_refs) > 0:
                graph.add_edge(
                    current_id, a_id, "Semantic requirement: View references backend model."
                )

        if "security/" in path_lower and "models/" in a_path_lower:
            graph.add_edge(
                current_id,
                a_id,
                "Semantic requirement: Security access rule targets backend model.",
            )

    return graph.get_dependencies_for(current_id)
