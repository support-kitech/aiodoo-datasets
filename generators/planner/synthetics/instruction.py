"""Synthesizes human-like engineering instructions deterministically using external templates."""

import logging
import random
from pathlib import Path
import yaml

from preprocessing.domain.repository import PreprocessedModule
from generators.common.discovery.classifier import Scenario

logger = logging.getLogger(__name__)


class InstructionEngine:
    """Loads YAML templates and renders deterministic instructions."""

    def __init__(self, templates_dir: Path | None = None) -> None:
        if templates_dir is None:
            # Default to the templates directory relative to this file
            templates_dir = Path(__file__).parent.parent / "templates"

        self.templates_dir = templates_dir
        self.templates: dict[str, list[str]] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Load all YAML files from the templates directory."""
        if not self.templates_dir.exists():
            logger.warning("Templates directory %s does not exist.", self.templates_dir)
            return

        for yaml_file in self.templates_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)

                if isinstance(data, dict):
                    for scenario_name, templates_list in data.items():
                        if scenario_name not in self.templates:
                            self.templates[scenario_name] = []
                        if isinstance(templates_list, list):
                            self.templates[scenario_name].extend(templates_list)
            except Exception as exc:
                logger.error("Failed to load template file %s: %s", yaml_file, exc)

    def generate(self, module: PreprocessedModule, scenario: Scenario) -> str:
        """Render a deterministic instruction for the given scenario."""
        available_templates = self.templates.get(scenario.name, [])

        if not available_templates:
            # Fallback if no template is explicitly defined for this scenario
            template = "Build the {module_name} module to satisfy the architectural requirements defined by its dependencies."
        else:
            # Use deterministic seeded selection based on module and scenario to ensure reproducibility
            seed_str = f"{module.name}_{scenario.name}_{module.metadata.get('version', '')}"
            rng = random.Random(seed_str)
            template = rng.choice(available_templates)

        return template.format(
            module_name=module.metadata.get("name", module.name),
            module_tech_name=module.name,
            version=module.metadata.get("version", ""),
            edition="ce",
        )


# Global singleton instance for backward compatibility with older pipeline code
_engine = None


def generate_instruction(module: PreprocessedModule, scenario: Scenario) -> str:
    """Backward compatible public interface for instruction generation."""
    global _engine
    if _engine is None:
        _engine = InstructionEngine()
    return _engine.generate(module, scenario)
