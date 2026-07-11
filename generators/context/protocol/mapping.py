"""Mapping utilities for Context Protocol V1."""

from generators.context.analysis.graph.graph import ContextGraph
from generators.context.generation.query import Query
from generators.context.ranking.result import RankingResult
from generators.context.protocol.schema import (
    ProtocolQuery,
    ProtocolArtifact,
    ProtocolNode,
    ProtocolEdge,
    ProtocolMetadata,
)
from generators.context.protocol.enums import (
    ProtocolQueryType,
    ProtocolIntent,
    ProtocolNodeType,
    ProtocolLanguage,
    ProtocolRankingReason,
)
from generators.context.protocol.constants import (
    CONTEXT_PROTOCOL_V1,
    GENERATOR_NAME,
)


def map_query(query: Query) -> ProtocolQuery:
    """Maps an engineering Query to ProtocolQuery."""
    return ProtocolQuery(
        query_id=query.query_id,
        query_type=ProtocolQueryType(query.query_type.value),
        intent=ProtocolIntent(query.intent.value),
        natural_language=query.natural_language,
        target_node=query.target_node,
        target_symbol=query.target_symbol,
    )


def map_artifact(result: RankingResult, graph: ContextGraph) -> ProtocolArtifact | None:
    """Maps a RankingResult to ProtocolArtifact if the node exists."""
    node = graph.get_node(result.node_id)
    if not node:
        return None

    return ProtocolArtifact(
        node_id=node.node_id,
        name=node.name,
        type=ProtocolNodeType(node.node_type.value),
        module=node.module,
        path=node.relative_path,
        language=ProtocolLanguage(node.language.value),
        start_line=result.metadata.get("start_line", 0),
        end_line=result.metadata.get("end_line", 0),
        score=result.score.value,
        ranking_reason=ProtocolRankingReason(result.reason.value),
    )


def map_node(node_id: str, graph: ContextGraph) -> ProtocolNode | None:
    """Maps a node ID to ProtocolNode."""
    node = graph.get_node(node_id)
    if not node:
        return None

    return ProtocolNode(
        node_id=node.node_id,
        name=node.name,
        type=ProtocolNodeType(node.node_type.value),
        module=node.module,
    )


def map_edge(edge) -> ProtocolEdge:  # type: ignore[no-untyped-def]
    """Maps an engineering edge to ProtocolEdge."""
    return ProtocolEdge(
        edge_id=edge.edge_id,
        source_id=edge.source_id,
        target_id=edge.target_id,
        relationship_type=edge.relationship_type.value,
    )


def map_metadata(
    module: str,
    query_type_value: str,
    artifact_count: int,
    relationship_count: int,
    protocol_hash: str,
) -> ProtocolMetadata:
    """Creates a ProtocolMetadata object."""
    return ProtocolMetadata(
        protocol_version=CONTEXT_PROTOCOL_V1,
        generator=GENERATOR_NAME,
        protocol_hash=protocol_hash,
        module=module,
        query_type=ProtocolQueryType(query_type_value),
        artifact_count=artifact_count,
        relationship_count=relationship_count,
    )
