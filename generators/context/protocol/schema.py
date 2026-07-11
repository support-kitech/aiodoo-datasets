"""Pydantic V2 Schemas for Context Protocol V1."""

from typing import Any
from pydantic import BaseModel, Field

from aiodoo_datasets.generators.context.protocol.constants import CONTEXT_PROTOCOL_V1, GENERATOR_NAME
from aiodoo_datasets.generators.context.protocol.enums import (
    ProtocolQueryType, ProtocolIntent, ProtocolNodeType, ProtocolLanguage, ProtocolRankingReason
)

class ProtocolQuery(BaseModel):
    """
    Represents the originating engineering question.
    Derived immutably from the internal Query object.
    """
    query_id: str = Field(..., description="Deterministic ID of the query.")
    query_type: ProtocolQueryType = Field(..., description="Type of query.")
    intent: ProtocolIntent = Field(..., description="The engineering intent of the query.")
    natural_language: str = Field(..., description="The formulated natural language question.")
    target_node: str = Field(..., description="The node ID this query targets.")
    target_symbol: str = Field(..., description="The symbol or name targeted by this query.")

class ProtocolArtifact(BaseModel):
    """
    Represents a ranked engineering artifact relevant to the query.
    Derived from a RankingResult and its corresponding ContextNode.
    """
    node_id: str = Field(..., description="Deterministic ID of the artifact node.")
    name: str = Field(..., description="The symbol or name of the artifact.")
    type: ProtocolNodeType = Field(..., description="The type of the node.")
    module: str = Field(..., description="The Odoo module where this artifact belongs.")
    path: str = Field(..., description="Relative file path of the artifact.")
    language: ProtocolLanguage = Field(..., description="Language of the artifact.")
    start_line: int = Field(..., description="Starting line number.")
    end_line: int = Field(..., description="Ending line number.")
    score: int = Field(..., description="Deterministic ranking score (0-100).")
    ranking_reason: ProtocolRankingReason = Field(..., description="Canonical reason the artifact was ranked.")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ProtocolArtifact):
            return False
        return self.node_id == other.node_id
        
    def __hash__(self) -> int:
        return hash(self.node_id)

class ProtocolNode(BaseModel):
    """Minimal representation of a graph node for context."""
    node_id: str = Field(..., description="Deterministic node ID.")
    name: str = Field(..., description="Name of the node.")
    type: ProtocolNodeType = Field(..., description="Type of the node.")
    module: str = Field(..., description="Module of the node.")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ProtocolNode):
            return False
        return self.node_id == other.node_id
        
    def __hash__(self) -> int:
        return hash(self.node_id)

class ProtocolEdge(BaseModel):
    """Minimal representation of a graph edge for context."""
    edge_id: str = Field(..., description="Deterministic edge ID.")
    source_id: str = Field(..., description="Source node ID.")
    target_id: str = Field(..., description="Target node ID.")
    relationship_type: str = Field(..., description="Type of relationship.")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ProtocolEdge):
            return False
        return self.edge_id == other.edge_id
        
    def __hash__(self) -> int:
        return hash(self.edge_id)

class ProtocolGraph(BaseModel):
    """
    Contains the minimal subgraph explaining the ranked artifacts.
    Never serializes the entire ContextGraph.
    """
    nodes: list[ProtocolNode] = Field(default_factory=list, description="Sorted list of minimal nodes.")
    edges: list[ProtocolEdge] = Field(default_factory=list, description="Sorted list of minimal edges.")

class ProtocolMetadata(BaseModel):
    """Dataset-level metadata for the record. No timestamps to ensure determinism."""
    protocol_version: str = Field(default=CONTEXT_PROTOCOL_V1, description="Protocol version.")
    generator: str = Field(default=GENERATOR_NAME, description="Name of the generator.")
    module: str = Field(..., description="Primary module for this task.")
    odoo_version: str = Field(default="17.0", description="Odoo target version.")
    query_type: ProtocolQueryType = Field(..., description="The type of the query in this task.")
    artifact_count: int = Field(..., description="Number of ranked artifacts.")
    relationship_count: int = Field(..., description="Number of relationships in the minimal graph.")

class ContextTask(BaseModel):
    """
    Root object representing exactly one deterministic dataset record.
    Forms the serialization boundary.
    """
    id: str = Field(..., description="Deterministic ID of the entire task.")
    query: ProtocolQuery = Field(..., description="The engineering question.")
    artifacts: list[ProtocolArtifact] = Field(default_factory=list, description="Ranked artifacts sorted by score and ID.")
    graph: ProtocolGraph = Field(..., description="Minimal context subgraph.")
    metadata: ProtocolMetadata = Field(..., description="Dataset-level metadata.")
