# Developer Guide

## Environment Setup
1. Use Python 3.12.
2. Install dependencies via `pip install .[dev]`.

## Adding Features
1. All domain objects must be implemented as `@dataclass(frozen=True, slots=True)`.
2. Do not introduce mutable state outside of `Statistics` objects.
3. Every component must be 100% unit tested.
4. Ensure no circular dependencies are introduced. The hierarchy is strictly top-down: `Integration -> Export -> Protocol -> Planning -> Graph -> Builders -> Analysis`.

## Testing
Run the complete test suite:
```bash
python -m unittest discover -s generators/execution/tests -v
```

## Running Static Analysis
```bash
ruff check generators/execution/
mypy generators/execution/
```
