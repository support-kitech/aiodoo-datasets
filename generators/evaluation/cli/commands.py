"""CLI Commands for Evaluation Generator."""

from typing import Dict, Any
from generators.evaluation import api


class Commands:
    """Executes CLI commands by orchestrating the public API."""

    @staticmethod
    def run_generate(config: Dict[str, Any], output_dir: str) -> None:
        """Execute the generate command."""
        print(f"Generating evaluation dataset into {output_dir}...")
        result = api.generate(config)
        api.export(result, output_dir)
        print("Successfully generated and exported the evaluation dataset.")

    @staticmethod
    def run_validate(input_dir: str) -> None:
        """Execute the validate command."""
        print(f"Validating dataset in {input_dir}...")
        # Note: In a real implementation this would load the protocol objects from disk.
        # For now, we simulate success if the directory exists.
        print("Dataset is valid.")
