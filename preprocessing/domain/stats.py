"""Statistics domain objects for the Preprocessing Framework."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TransformationStatistics:
    """Observational statistics for transformations applied to a file or module."""
    
    whitespace_removed_bytes: int = 0
    comments_normalized: int = 0
    tokens_estimated: int = 0
    duplicates_detected: int = 0

    def add(self, **kwargs) -> "TransformationStatistics":
        """Return a new instance with the specified values added to the current values."""
        current_dict = {
            "whitespace_removed_bytes": self.whitespace_removed_bytes,
            "comments_normalized": self.comments_normalized,
            "tokens_estimated": self.tokens_estimated,
            "duplicates_detected": self.duplicates_detected,
        }
        for k, v in kwargs.items():
            if k in current_dict:
                current_dict[k] += v
        from dataclasses import replace
        return replace(self, **current_dict)



