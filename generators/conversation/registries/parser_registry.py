"""Parser registry for Conversation Generator."""

from typing import Type, Dict, Callable


class ParserRegistry:
    """Static registry for protocol parsers."""

    _registry: Dict[str, Type] = {}  # type: ignore[type-arg]

    @classmethod
    def register(cls, protocol_key: str) -> Callable:  # type: ignore[type-arg]
        """Decorator to register a parser class for a specific protocol key."""

        def decorator(parser_cls: Type) -> Type:  # type: ignore[type-arg]
            cls._registry[protocol_key] = parser_cls
            return parser_cls

        return decorator

    @classmethod
    def get_parser(cls, protocol_key: str) -> Type:  # type: ignore[type-arg]
        """Get a parser for a specific protocol key."""
        return cls._registry.get(protocol_key)  # type: ignore[return-value]

    @classmethod
    def get_all_parsers(cls) -> Dict[str, Type]:  # type: ignore[type-arg]
        """Get all registered parsers."""
        return dict(cls._registry)
