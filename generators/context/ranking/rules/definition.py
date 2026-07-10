"""Definition Ranking Rule."""

from aiodoo_datasets.generators.context.analysis.graph.graph import ContextGraph
from aiodoo_datasets.generators.context.generation.query import Query, QueryType
from aiodoo_datasets.generators.context.ranking.enums import RankingRuleType, RankingScore, RankingReason
from aiodoo_datasets.generators.context.ranking.result import RankingResult
from aiodoo_datasets.generators.context.ranking.base import BaseRankingRule
from aiodoo_datasets.generators.context.ranking.utils import freeze_metadata

class DefinitionRule(BaseRankingRule):
    """
    Ranks direct structural definitions at the highest priority.
    
    Engineering Purpose:
        Identifies the exact definition node for Models and Fields.
        Receives the highest confidence (100) as this is the canonical source.
        
    Supported Queries:
        FIND_MODEL
        FIND_FIELD
        
    Limitations:
        Does not traverse relationships, only maps the query target directly.
    """
    rule_type = RankingRuleType.DEFINITION
    supported_query_types = [QueryType.FIND_MODEL, QueryType.FIND_FIELD]

    def rank(self, query: Query, graph: ContextGraph) -> list[RankingResult]:
        results = []
        if query.query_type in self.supported_query_types:
            node = graph.get_node(query.target_node)
            if node:
                results.append(
                    RankingResult(
                        query_id=query.query_id,
                        node_id=node.node_id,
                        score=RankingScore.DEFINITION,
                        matched_rule=self.rule_type,
                        reason=RankingReason.DIRECT_DEFINITION,
                        metadata=freeze_metadata({
                            "module": node.module,
                            "language": node.language.value,
                            "relative_path": node.relative_path,
                            "start_line": 0 # Defaulting to 0 since line is not mapped in Node yet
                        })
                    )
                )
        return results
