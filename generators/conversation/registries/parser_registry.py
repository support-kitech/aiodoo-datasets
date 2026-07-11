"""Parser registry for Conversation Generator."""

from typing import Type, Dict, Callable


class ParserRegistry:
    """Static registry for protocol parsers."""

    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, protocol_key: str) -> Callable:
        """Decorator to register a parser class for a specific protocol key."""

        def decorator(parser_cls: Type) -> Type:
            cls._registry[protocol_key] = parser_cls
            return parser_cls

        return decorator

    @classmethod
    def get_parser(cls, protocol_key: str) -> Type:
        """Get a parser for a specific protocol key."""
        return cls._registry.get(protocol_key)

    @classmethod
    def get_all_parsers(cls) -> Dict[str, Type]:
        """Get all registered parsers."""
        return dict(cls._registry)
