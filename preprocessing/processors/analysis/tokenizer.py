"""Token estimator strategy and processor."""

from preprocessing.constants.framework import ANALYSIS_PROCESSOR_PRIORITY
import abc
from preprocessing.processors.base import BaseProcessor, ProcessorContext


class TokenizerProvider(abc.ABC):
    """Abstract provider for tokenizer implementation."""

    @abc.abstractmethod
    def estimate(self, text: str) -> int:
        """Estimate the number of tokens in the given text."""
        pass


class OpenAITokenizer(TokenizerProvider):
    """Tokenizer provider using cl100k_base approximation."""

    def estimate(self, text: str) -> int:
        if not text:
            return 0
        return max(1, len(text) // 4)


class TokenEstimatorProcessor(BaseProcessor):
    """Processor that applies a TokenizerProvider to calculate statistics."""

    def __init__(self, provider: TokenizerProvider | None = None):
        self.provider = provider or OpenAITokenizer()

    @property
    def priority(self) -> int:
        return ANALYSIS_PROCESSOR_PRIORITY

    def process(self, context: ProcessorContext) -> ProcessorContext:
        tokens = self.provider.estimate(context.current_content)
        new_stats = context.statistics.add(tokens_estimated=tokens)
        return context.with_update(statistics=new_stats)
