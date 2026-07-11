"""Orchestrates query generation across the ContextGraph."""

import logging

from generators.context.analysis.graph.graph import ContextGraph
from generators.context.generation.query import Query
from generators.context.generation.registry import REGISTERED_QUERY_PLUGINS

logger = logging.getLogger(__name__)


class QueryGenerator:
    """
    Orchestrates the execution of statically registered Query Plugins.

    Responsibilities:
    - Executes query plugins in a deterministic, alphabetical order.
    - Collects generated queries and explicitly drops duplicates.
    - Sorts queries deterministically before returning.
    - Provides fault tolerance if a plugin fails.
    """

    def __init__(self) -> None:
        # Register plugins statically and ensure deterministic alphabetical sorting.
        self.plugins = sorted(
            [plugin_cls() for plugin_cls in REGISTERED_QUERY_PLUGINS],
            key=lambda p: p.__class__.__name__,
        )

    def generate_queries(self, graph: ContextGraph) -> list[Query]:
        """
        Execute all registered query plugins.

        Args:
            graph: A fully populated ContextGraph.

        Returns:
            A deterministically sorted list of unique Query objects.
        """
        generated_queries = []
        seen_signatures = set()

        for plugin in self.plugins:
            try:
                queries = plugin.generate(graph)

                for q in queries:
                    # Task 5: Stronger duplicate detection
                    sig = (q.query_type.value, q.intent.value, q.target_node, q.target_symbol)
                    if sig not in seen_signatures:
                        seen_signatures.add(sig)
                        generated_queries.append(q)

            except Exception as e:
                query_type = getattr(plugin, "query_type", "Unknown")
                if hasattr(query_type, "value"):
                    query_type = query_type.value

                module = getattr(e, "module", "Unknown")
                target = getattr(e, "target_symbol", "Unknown")

                logger.exception(
                    "Query Plugin Failed\nPlugin: %s\nQuery Type: %s\nTarget: %s\nModule: %s",
                    plugin.__class__.__name__,
                    query_type,
                    target,
                    module,
                )

        # Deterministically sort all generated queries before returning
        return sorted(generated_queries)
