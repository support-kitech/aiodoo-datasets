"""Mapper for converting engineering objects to Context Protocol V1."""

import hashlib
import logging

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.generation.query import Query
from aiodoo_datasets.generators.context.ranking.result import RankingResult
from aiodoo_datasets.generators.context.protocol.schema import (
    ContextTask,
    ProtocolGraph
)
from aiodoo_datasets.generators.context.protocol.mapping import (
    map_query, map_artifact, map_node, map_edge, map_metadata
)

logger = logging.getLogger(__name__)

class ContextMapper:
    """
    Read-only mapper that transforms engineering objects into the deterministic Context Protocol V1.
    Never mutates the input objects.
    Extracts the minimal subgraph required to explain the ranked artifacts.
    """

    def map(self, query: Query, results: list[RankingResult], graph: ContextGraph) -> ContextTask:
        """
        Transforms Query + RankingResults + ContextGraph into ContextTask.
        
        Args:
            query: The originating query.
            results: A list of deterministically ranked RankingResult objects.
            graph: The read-only ContextGraph.
            
        Returns:
            A deterministic ContextTask representing Protocol V1.
        """
        try:
            # 1. Map Query
            proto_query = map_query(query)

            # 2. Map Artifacts and Identify Subgraph components
            proto_artifacts = []
            relevant_node_ids = set([query.target_node])
            relevant_edges = []

            # Add target node if available
            target_graph_node = graph.get_node(query.target_node)
            module = "unknown"
            if target_graph_node:
                module = target_graph_node.module

            for result in results:
                proto_artifact = map_artifact(result, graph)
                if not proto_artifact:
                    continue
                    
                relevant_node_ids.add(proto_artifact.node_id)
                proto_artifacts.append(proto_artifact)
                
                # Reconstruct traversed edge based on metadata (Design decision from User Review)
                matched_relationship = result.metadata.get("matched_relationship")
                if matched_relationship:
                    # Look for edges connecting the query target and this artifact
                    for edge in graph.find_edges_by_type(matched_relationship):
                        if (edge.source_id == result.node_id and edge.target_id == query.target_node) or \
                           (edge.target_id == result.node_id and edge.source_id == query.target_node):
                            relevant_edges.append(map_edge(edge))

            # 3. Build Minimal Graph
            proto_nodes = []
            for nid in relevant_node_ids:
                p_node = map_node(nid, graph)
                if p_node:
                    proto_nodes.append(p_node)

            # Deduplicate and sort edges
            unique_edges = {e.edge_id: e for e in relevant_edges}
            sorted_edges = sorted(list(unique_edges.values()), key=lambda e: e.edge_id)
            
            # Sort nodes
            sorted_nodes = sorted(proto_nodes, key=lambda n: n.node_id)

            proto_graph = ProtocolGraph(
                nodes=sorted_nodes,
                edges=sorted_edges
            )

            # 4. Build Metadata
            proto_metadata = map_metadata(
                module=module,
                query_type_value=query.query_type.value,
                artifact_count=len(proto_artifacts),
                relationship_count=len(sorted_edges)
            )

            # 5. Build Final ContextTask
            # Task ID is deterministically derived from query ID
            task_id = hashlib.sha256(f"task:{query.query_id}".encode("utf-8")).hexdigest()

            return ContextTask(
                id=task_id,
                query=proto_query,
                artifacts=proto_artifacts,
                graph=proto_graph,
                metadata=proto_metadata
            )

        except Exception:
            # Task 7 - Mapper Logging
            artifact_count = len(results)
            logger.exception(
                "Mapper Failed\n"
                "Query ID: %s\n"
                "Module: %s\n"
                "Artifact Count: %s",
                query.query_id,
                module if 'module' in locals() else "unknown",
                artifact_count
            )
            raise
