"""Processor pipeline for orchestrating processor execution."""

from preprocessing.processors.base import ProcessorContext
from preprocessing.processors.registry import ProcessorRegistry


class ProcessorPipeline:
    """
    Coordinates the sequential execution of registered processors on a ProcessorContext.
    Enforces immutability by ensuring each processor returns a new context.
    """

    def __init__(self, registry: ProcessorRegistry):
        self._registry = registry

    def execute(self, initial_context: ProcessorContext) -> ProcessorContext:
        """
        Execute the full sequence of processors for the context's language.

        Args:
            initial_context: The raw, initial ProcessorContext.

        Returns:
            The final, normalized ProcessorContext.
        """
        processors = self._registry.get_processors_for_language(initial_context.language)

        current_context = initial_context
        for processor in processors:
            current_context = processor.process(current_context)

        return current_context

    def execute_many(
        self, initial_contexts: tuple[ProcessorContext, ...]
    ) -> tuple[ProcessorContext, ...]:
        """
        Execute processors for multiple contexts sequentially.
        Prepared for future parallelization/scalability without architectural changes.
        """
        return tuple(self.execute(ctx) for ctx in initial_contexts)
