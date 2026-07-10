"""Static registry for query plugins."""

from aiodoo_datasets.generators.context.generation.queries import (
    FindModelQuery,
    FindFieldQuery,
    FindComputeQuery,
    FindViewQuery,
    FindActionQuery,
    FindMenuQuery,
    FindSecurityQuery,
    FindDependencyQuery,
)

# Constant defining all explicitly registered query plugins.
# No reflection or dynamic importing is allowed to ensure determinism.
REGISTERED_QUERY_PLUGINS = (
    FindActionQuery,
    FindComputeQuery,
    FindDependencyQuery,
    FindFieldQuery,
    FindMenuQuery,
    FindModelQuery,
    FindSecurityQuery,
    FindViewQuery,
)
