"""Unified command-line interface for AIODOO Dataset Generators."""

import argparse
import logging

def build_base_parser(description: str) -> argparse.ArgumentParser:
    """Creates a standardized argument parser for dataset generators."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--sources", type=str, required=True, help="Path to the sources.yaml defining Odoo repositories")
    parser.add_argument("--output", type=str, required=True, help="Directory to output the dataset, cache, and checkpoints")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent multiprocessing workers")
    parser.add_argument("--resume", action="store_true", help="Resume pipeline generation from the last saved checkpoint")
    parser.add_argument("--reset-checkpoint", action="store_true", help="Clear any existing checkpoints and start fresh")
    
    return parser

def setup_logging(level: int = logging.INFO) -> None:
    """Configure standard logging for all AIODOO CLI tools."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
