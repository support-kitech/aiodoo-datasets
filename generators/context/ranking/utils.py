"""Utility functions for Ranking Engine."""

from types import MappingProxyType


def freeze_metadata(data: dict) -> MappingProxyType:
    """Recursively freezes a dictionary using MappingProxyType."""
    if not isinstance(data, dict):
        return data
    frozen_dict = {}
    for key, value in data.items():
        if isinstance(value, dict):
            frozen_dict[key] = freeze_metadata(value)
        elif isinstance(value, list):
            # Tuples are immutable sequence replacements for lists in metadata
            frozen_dict[key] = tuple(value)
        else:
            frozen_dict[key] = value
    return MappingProxyType(frozen_dict)
