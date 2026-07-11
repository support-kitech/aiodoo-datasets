"""Parser registry for the Approval Generator."""

from typing import Dict, Type
from aiodoo_datasets.generators.approval.analysis.parsers.base_parser import BaseParser


class ParserRegistry:
    """Registry to hold all available evidence parsers."""

    _parsers: Dict[str, Type[BaseParser]] = {}

    @classmethod
    def register(cls, parser_key: str):
        """Decorator to register a parser."""

        def decorator(parser_class: Type[BaseParser]):
            cls._parsers[parser_key] = parser_class
            return parser_class

        return decorator

    @classmethod
    def get_parser(cls, parser_key: str) -> BaseParser:
        """Get an instance of a registered parser."""
        parser_class = cls._parsers.get(parser_key)
        if not parser_class:
            return None
        return parser_class()

    @classmethod
    def get_all_parsers(cls) -> Dict[str, BaseParser]:
        """Get instances of all registered parsers."""
        return {key: parser_class() for key, parser_class in cls._parsers.items()}
