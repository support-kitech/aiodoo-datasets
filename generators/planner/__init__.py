"""
AIODOO Datasets: Planner Generator Subsystem.

Transforms extracted Discovery intelligence into strictly validated
Planning Protocol V1 JSONL datasets. No LLMs, No Regex, 100% Deterministic.
"""

from .pipeline import PlannerPipeline

__all__ = ["PlannerPipeline"]
