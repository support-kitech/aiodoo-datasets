"""Build Conversation JSONL records from training slices."""

from __future__ import annotations

import hashlib
from typing import Any

from generators.conversation.analysis.slicer import TrainingSlice
from generators.conversation.domain.metadata import ConversationMetadata
from generators.conversation.policy import ID_SCHEME_VERSION
from generators.conversation.version import SCHEMA_VERSION, __version__


class SliceRecordBuilder:
    """Serialize one TrainingSlice into a contract-projectable JSONL record."""

    @staticmethod
    def build(
        training_slice: TrainingSlice,
        *,
        base_metadata: ConversationMetadata,
    ) -> dict[str, Any]:
        messages = list(training_slice.prefix) + [training_slice.reply]
        output = {
            "conversation_id": training_slice.conversation_id,
            "turn_index": training_slice.turn_index,
            "turns": [
                {
                    "turn_id": f"{training_slice.conversation_id}:t{training_slice.turn_index}",
                    "messages": [
                        {
                            "role": m["role"],
                            "content": m["content"],
                        }
                        for m in messages
                    ],
                }
            ],
        }
        metadata = {
            "module": training_slice.module,
            "source_module": training_slice.module,
            "protocol_hash": _protocol_hash(training_slice.record_id),
            "generator_version": __version__,
            "protocol_version": base_metadata.protocol_version,
            "schema_version": SCHEMA_VERSION,
            "conversation_type": base_metadata.conversation_type.value,
            "conversation_id": training_slice.conversation_id,
            "turn_index": training_slice.turn_index,
            "record_id": training_slice.record_id,
            "id_scheme_version": ID_SCHEME_VERSION,
        }
        return {
            "instruction": (
                "Continue the Odoo development conversation with the next assistant reply."
            ),
            "context": {
                "conversation_id": training_slice.conversation_id,
                "turn_index": training_slice.turn_index,
                "module": training_slice.module,
            },
            "output": output,
            "metadata": metadata,
            "record_id": training_slice.record_id,
            "conversation_id": training_slice.conversation_id,
            "turn_index": training_slice.turn_index,
        }


def _protocol_hash(record_id: str) -> str:
    return hashlib.sha256(record_id.encode("utf-8")).hexdigest()
