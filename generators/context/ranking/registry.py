"""Static registry for ranking rules."""

from aiodoo_datasets.generators.context.ranking.rules import (
    DefinitionRule,
    InheritanceRule,
    DependencyRule,
    ViewRule,
    SecurityRule,
    ActionRule
)

# Constant defining all explicitly registered ranking rules.
# No reflection or dynamic importing is allowed to ensure determinism.
REGISTERED_RANKING_RULES = (
    ActionRule,
    DefinitionRule,
    DependencyRule,
    InheritanceRule,
    SecurityRule,
    ViewRule,
)
