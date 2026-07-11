"""Processor registry for the Preprocessing Framework."""


from preprocessing.domain.file import Language
from preprocessing.processors.base import BaseProcessor


class ProcessorRegistry:
    """
    Maintains the deterministic execution order of processors.
    Processors register themselves and the pipeline requests them by category/language.
    """
    
    def __init__(self):
        # We store processor instances deterministically.
        # Order matters!
        self._universal_processors: list[BaseProcessor] = []
        self._language_processors: dict[Language, list[BaseProcessor]] = {
            lang: [] for lang in Language
        }
        self._analysis_processors: list[BaseProcessor] = []
        self._frozen: bool = False
        
    def _assert_not_frozen(self) -> None:
        from preprocessing.exceptions import PreprocessingError
        if self._frozen:
            raise PreprocessingError("ProcessorRegistry is frozen and cannot be modified.")
            
    def register_universal(self, processor: BaseProcessor) -> None:
        """Register a processor that runs on every file (e.g., WhitespaceProcessor)."""
        self._assert_not_frozen()
        self._universal_processors.append(processor)
        
    def register_language(self, language: Language, processor: BaseProcessor) -> None:
        """Register a processor specific to a language (e.g., PythonProcessor)."""
        self._assert_not_frozen()
        self._language_processors[language].append(processor)
        
    def register_analysis(self, processor: BaseProcessor) -> None:
        """Register an analysis processor that runs after all normalizations."""
        self._assert_not_frozen()
        self._analysis_processors.append(processor)
        
    def freeze(self) -> None:
        """
        Locks the registry, preventing further registrations.
        Sorts all processor lists by their deterministic priority.
        """
        self._assert_not_frozen()
        
        # Sort by priority
        self._universal_processors.sort(key=lambda p: p.priority)
        for lang_list in self._language_processors.values():
            lang_list.sort(key=lambda p: p.priority)
        self._analysis_processors.sort(key=lambda p: p.priority)
        
        self._frozen = True
        
    def get_processors_for_language(self, language: Language) -> tuple[BaseProcessor, ...]:
        """
        Get the exact, deterministic sequence of processors for a file.
        Order: Universal -> Language Specific -> Analysis
        """
        sequence = []
        sequence.extend(self._universal_processors)
        sequence.extend(self._language_processors.get(language, []))
        sequence.extend(self._analysis_processors)
        return tuple(sequence)
