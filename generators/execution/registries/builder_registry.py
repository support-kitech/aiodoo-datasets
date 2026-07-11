from aiodoo_datasets.generators.execution.registries.base import BaseRegistry


class BuilderRegistry(BaseRegistry):
    """
    Validates and manages the deterministic ordering of Builders.
    """

    def validate(self) -> None:
        """
        Validates priority uniqueness and REQUIRES dependency ordering.
        Also validates INPUT/OUTPUT chains.
        """
        priorities = set()
        types = set()

        # Pass 1: Validate uniqueness, priorities, and INPUT/OUTPUT declarations
        for builder in self._items:
            if builder.__class__ in types:
                raise ValueError(f"Duplicate Builder type registered: {builder.__class__.__name__}")
            types.add(builder.__class__)

            if not hasattr(builder, "PRIORITY"):
                raise ValueError(f"{builder.__class__.__name__} missing PRIORITY")

            if builder.PRIORITY in priorities:
                raise ValueError(
                    f"Duplicate PRIORITY {builder.PRIORITY} found in {builder.__class__.__name__}"
                )
            priorities.add(builder.PRIORITY)

            if not hasattr(builder, "INPUT") or not hasattr(builder, "OUTPUT"):
                raise ValueError(f"{builder.__class__.__name__} missing INPUT/OUTPUT declarations")

        # Sort by PRIORITY before checking REQUIRES ordering
        self._items.sort(key=lambda b: b.PRIORITY)

        # Pass 2: Validate REQUIRES against the full type set and ordering
        seen = set()
        for builder in self._items:
            if hasattr(builder, "REQUIRES"):
                for req in builder.REQUIRES:
                    if req not in types:
                        raise ValueError(
                            f"{builder.__class__.__name__} REQUIRES {req.__name__}, but it is not registered."
                        )
                    if req not in seen:
                        raise ValueError(
                            f"{builder.__class__.__name__} REQUIRES {req.__name__}, but it has a higher PRIORITY (runs later)."
                        )
            seen.add(builder.__class__)
