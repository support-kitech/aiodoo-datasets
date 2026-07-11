"""Orchestrates relationship extraction across the context graph."""

import logging

from generators.context.analysis.knowledge import ContextKnowledge
from generators.context.analysis.graph.graph import ContextGraph
from generators.context.analysis.relationships import (
    ComputesRelationship,
    ContainsRelationship,
    DisplaysRelationship,
    InheritsRelationship,
    TriggersRelationship,
)

logger = logging.getLogger(__name__)

REGISTERED_RELATIONSHIP_EXTRACTORS = (
    ComputesRelationship,
    ContainsRelationship,
    DisplaysRelationship,
    InheritsRelationship,
    TriggersRelationship,
)


class GraphBuilder:
    """
    Orchestrates the execution of statically registered Relationship Extractors.

    Responsibilities:
    - Executes extractors in a deterministic, alphabetical order.
    - Deterministically adds returned edges to the ContextGraph.
    - Prevents duplicate edges and invalid edge insertions securely.
    - Provides fault tolerance if an extractor fails.
    """

    def __init__(self) -> None:
        # Register extractors statically and ensure deterministic alphabetical sorting.
        self.extractors = sorted(
            [extractor_cls() for extractor_cls in REGISTERED_RELATIONSHIP_EXTRACTORS],
            key=lambda e: e.__class__.__name__,
        )

    def build_relationships(self, graph: ContextGraph, knowledge: ContextKnowledge) -> None:
        """
        Execute all registered extractors and populate the graph with edges.

        Args:
            graph: A ContextGraph pre-populated with ContextNode objects.
            knowledge: Strongly typed knowledge object for the module.
        """
        for extractor in self.extractors:
            try:
                edges = extractor.extract(graph, knowledge)

                # Deterministically sort the extracted edges before insertion to guarantee stability
                for edge in sorted(edges):
                    if not graph.contains_node(edge.source_id):
                        logger.warning(
                            "Edge skipped: Source node %s does not exist. (Extractor: %s)",
                            edge.source_id,
                            extractor.__class__.__name__,
                        )
                        continue

                    if not graph.contains_node(edge.target_id):
                        logger.warning(
                            "Edge skipped: Target node %s does not exist. (Extractor: %s)",
                            edge.target_id,
                            extractor.__class__.__name__,
                        )
                        continue

                    if graph.contains_edge(edge.edge_id):
                        continue  # Duplicate edges are safely ignored to preserve determinism

                    try:
                        graph.add_edge(edge)
                    except ValueError as ve:
                        logger.warning("Failed to add edge: %s", str(ve))

            except Exception:
                logger.exception(
                    "Relationship extractor '%s' failed on module '%s'.",
                    extractor.__class__.__name__,
                    knowledge.module_name,
                )
