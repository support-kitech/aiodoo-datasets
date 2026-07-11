"""Wrapper to integrate AIODOO Core Protocol Validator into the Datasets pipeline."""

import logging
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# We attempt to dynamically import the core components.
# If they are not found in the environment, we attempt to resolve the local workspace.
try:
    from aiodoo.protocol.validator import ProtocolValidator, ValidationError
    from aiodoo.protocol.schemas import AgentContext, AIODOOEvent, PlanPayload
except ImportError:
    # Try resolving local path assuming aiodoo-core is in the same parent directory
    core_path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent / "aiodoo-core"
    if core_path.exists() and str(core_path) not in sys.path:
        sys.path.append(str(core_path))

    try:
        from protocol.validator import ProtocolValidator, ValidationError
        from protocol.schemas import AgentContext, AIODOOEvent, PlanPayload
    except ImportError:
        logger.warning(
            "Could not import AIODOO Core Protocol Validator. Core validation will be bypassed."
        )
        ProtocolValidator = None
        ValidationError = Exception
        AgentContext = None
        AIODOOEvent = None
        PlanPayload = None


class DummyToolRegistry:
    """A mocked registry to satisfy ProtocolValidator during synthetic generation."""

    def get(self, action_name: str) -> Any:
        class DummyTool:
            def validate_args(self, context: Any, action: Any) -> None:
                pass

        return DummyTool()


class DummySettings:
    """Mocked settings for ProtocolValidator."""

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
            # Patch resolve_workspace and resolve_path_in_workspace to bypass IO checks
            self._context.resolve_workspace = lambda ws: Path("/tmp/synthetic")
            self._context.resolve_path_in_workspace = lambda ws, path: Path("/tmp/synthetic") / path

            self._validator = ProtocolValidator(context=self._context)

    def validate_plan(self, payload_dict: dict[str, Any]) -> None:
        """Validates a raw dataset output dictionary against Core Protocol V1."""
        if not self.is_available:
            return

        try:
            # We must reconstruct the core Pydantic/Dataclass from the dict
            plan_payload = PlanPayload(**payload_dict)
            event = AIODOOEvent(
                id="synthetic_event", event_type="plan", payload=plan_payload, version="1.0"
            )
            self._validator.validate(event)
        except ValidationError as e:
            # Re-raise as standard ValueError to abstract core dependencies from pipeline
            raise ValueError(f"Core Protocol Validation Failed: {e}") from e
        except Exception as e:
            raise ValueError(f"Failed to parse payload into Core models: {e}") from e
