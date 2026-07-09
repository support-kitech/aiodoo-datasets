"""Deterministic instruction generation for Coding Model datasets."""

from pathlib import Path
import yaml
import hashlib

from aiodoo_datasets.generators.coding.discovery import OdooModule, Scenario

class InstructionEngine:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates = self._load_templates()

    def _load_templates(self) -> dict[str, list[str]]:
        templates = {}
        for yaml_file in self.templates_dir.glob("*.yaml"):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    templates[yaml_file.stem] = [t["text"] for t in data.get("templates", [])]
            except Exception:
                pass
        return templates

    def generate(self, module: OdooModule, scenario: Scenario) -> str:
        # Fallback template if missing
        generic = [
            "Implement the backend logic for the {module_name} module, focusing on the core business objects defined in {feature}.",
            "Create the data models and views required to implement {feature} for the {module_name} addon."
        ]
        
        # We look for a template matching the scenario name, else fallback to 'coding'
        category = scenario.name.lower().replace(" ", "_")
        available = self.templates.get(category, self.templates.get("coding", generic))
        
        if not available:
            available = generic
            
        # Stable hash for strict determinism (no random module)
        seed_str = f"{module.name}_{scenario.name}_{module.version}"
        seed_val = int(hashlib.md5(seed_str.encode("utf-8")).hexdigest(), 16)
        
        template_index = seed_val % len(available)
        template = available[template_index]
        
        return template.format(
            module_name=module.name,
            feature=scenario.name
        )

def generate_instruction(module: OdooModule, scenario: Scenario) -> str:
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    engine = InstructionEngine(templates_dir)
    return engine.generate(module, scenario)
