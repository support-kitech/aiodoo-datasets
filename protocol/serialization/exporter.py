"""Exporter for the Protocol Framework."""

from typing import Any

from protocol.domain.dataset import ProtocolContext
from protocol.domain.enums import ExportFormat
from protocol.serialization.serializer import Serializer


class Exporter:
    """
    Stateless export layer that produces output payloads
    from a ProtocolContext in a specified format.

    The Exporter only consumes ProtocolContext.
    It never understands Builders, Registry, or validation internals.
    """

    @staticmethod
    def export(
        context: ProtocolContext, fmt: ExportFormat = ExportFormat.JSON
    ) -> str | dict[str, Any]:
        """
        Export a ProtocolContext in the specified format.

        Args:
            context: The root protocol graph.
            fmt: Output format enum.

        Returns:
            A JSON string, a JSONL line, or a plain dictionary.
        """
        if fmt == ExportFormat.JSON:
            return Serializer.to_json(context)
        elif fmt == ExportFormat.JSONL:
            return Serializer.to_jsonl(context)
        elif fmt == ExportFormat.DICT:
            return Serializer.context_to_dict(context)
        else:
            raise ValueError(f"Unsupported export format: {fmt!r}")
