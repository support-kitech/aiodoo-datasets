"""Deprecation framework."""

import warnings
from typing import Any, Callable


def deprecated(reason: str) -> Callable:
    """
    Decorator to mark functions or classes as deprecated.

    Args:
        reason: Reason for deprecation and migration instructions.
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"{func.__name__} is deprecated: {reason}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
