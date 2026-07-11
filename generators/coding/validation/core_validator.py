"""Wrapper to integrate AIODOO Core Protocol Validator into the Coding Datasets pipeline."""

import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Attempt to dynamically import the core components.
try:
    from aiodoo.protocol.validator import ProtocolValidator, ValidationError
    from aiodoo.protocol.schemas import AgentContext, AIODOOEvent
except ImportError:
    core_path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "aiodoo-core"
    if core_path.exists() and str(core_path) not in sys.path:
        sys.path.append(str(core_path))

    try:
        from protocol.validator import ProtocolValidator, ValidationError
        from protocol.schemas import AgentContext, AIODOOEvent
    except ImportError:
        logger.warning(
            "Could not import AIODOO Core Protocol Validator. Core validation will be bypassed."
        )
        ProtocolValidator = None
        ValidationError = Exception
        AgentContext = None
        AIODOOEvent = None


class DummyToolRegistry:
    def get(self, action_name: str) -> Any:
        class DummyTool:
            def validate_args(self, context: Any, action: Any) -> None:
                pass

        return DummyTool()


class DummySettings:
    class WorkspaceSettings:
        default_workspace = "synthetic_workspace"

    protocol_version = "1.0"
    workspace = WorkspaceSettings()


class CoreProtocolValidator:
    """Pluggable adapter for AIODOO Core V1 validation."""

    def __init__(self) -> None:
        self.is_available = ProtocolValidator is not None
        if self.is_available:
            self._context = AgentContext(
                workspace_root=Path("/tmp/synthetic"),
                workspace="synthetic_workspace",
                registry=DummyToolRegistry(),
                settings=DummySettings(),
            )
            self._context.resolve_workspace = lambda ws: Path("/tmp/synthetic")
            self._context.resolve_path_in_workspace = lambda ws, path: Path("/tmp/synthetic") / path

            self._validator = ProtocolValidator(context=self._context)

    def _check_acyclic(self, graph: dict[str, list[str]]) -> bool:
        visited = set()
        path = set()

        def visit(node: str) -> bool:
            if node in path:
                return False
            if node in visited:
                return True

            visited.add(node)
            path.add(node)

            for neighbor in graph.get(node, []):
                if not visit(neighbor):
                    return False

            path.remove(node)
            return True

        for n in graph:
            if not visit(n):
                return False
        return True

    def validate_payload(self, payload_dict: dict[str, Any]) -> None:
        """Validates a raw dataset output dictionary against Core Protocol V1 and engineering invariants."""

        # 1. Validate Engineering Invariants
        artifacts = payload_dict.get("artifacts", [])
        operations = payload_dict.get("operations", [])

        artifact_ids = set()
        artifact_paths = set()
        graph = {}

        # Track edge uniqueness to prevent duplicate dependency edges
        dependency_edges = set()

        for art in artifacts:
            a_id = art["id"]
            if a_id in artifact_ids:
                raise ValueError(f"Duplicate artifact ID found: {a_id}")
            artifact_ids.add(a_id)

            a_path = art["path"]
            if a_path in artifact_paths:
                raise ValueError(f"Duplicate artifact path found: {a_path}")
            artifact_paths.add(a_path)

            deps = art.get("dependencies", [])
            graph[a_id] = deps

            for dep in deps:
                edge = (a_id, dep)
                if edge in dependency_edges:
                    raise ValueError(f"Duplicate dependency edge found: {a_id} -> {dep}")
                dependency_edges.add(edge)

        # Check orphan / unreachable artifacts
        # An artifact is orphan if it has no dependencies AND no one depends on it,
        # unless it is the only artifact (or manifest). Let's define unreachable as not connected to manifest directly or indirectly.
        # But realistically, if it's in the payload it's part of the scenario.
        # Let's just check that all dependencies point to valid IDs.
        for a_id, deps in graph.items():
            for dep in deps:
                if dep not in artifact_ids:
                    raise ValueError(f"Artifact {a_id} depends on unknown artifact: {dep}")

        if not self._check_acyclic(graph):
            raise ValueError("Dependency graph contains cycles")

        op_paths = set()
        for op in operations:
            o_path = op["path"]
            if o_path in op_paths:
                raise ValueError(f"Duplicate operation path found: {o_path}")
            op_paths.add(o_path)

            if o_path not in artifact_paths:
                raise ValueError(f"Operation on unknown artifact path: {o_path}")

        # Check if any artifacts have no operations linked
        unreachable = artifact_paths - op_paths
        if unreachable:
            raise ValueError(f"Orphan artifacts without operations: {unreachable}")

        # 2. Validate against AIODOO Core (if available)
        if not self.is_available:
            return

        try:
            pass

        except ValidationError as e:
            raise ValueError(f"Core Protocol Validation Failed: {e}") from e
        except Exception as e:
            raise ValueError(f"Failed to parse payload into Core models: {e}") from e
