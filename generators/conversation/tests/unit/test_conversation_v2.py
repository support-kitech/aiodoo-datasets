"""Unit tests for Conversation v2 episode reconstruction, slicing, and pipeline."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from generators.conversation.analysis.episode import EpisodeReconstructor
from generators.conversation.analysis.slicer import DialogueSlicer
from generators.conversation.builders.metadata_builder import MetadataBuilder
from generators.conversation.enums import ConversationType
from generators.conversation.history import truncate_prefix
from generators.conversation.identity import compute_conversation_id, compute_record_id
from generators.conversation.pipeline import ConversationPipeline
from generators.conversation.pipeline_context import PipelineContext
from generators.conversation.policy import MAX_HISTORY_MESSAGES, MAX_MESSAGE_CHARS
from generators.common.contract.adapters import project_conversation


def _row(
    *,
    capability: str,
    module: str,
    protocol_hash: str,
    instruction: str = "do work",
) -> dict:
    if capability == "planner":
        output = {"goal": instruction, "tasks": [{"id": "t1", "description": "plan step"}]}
    elif capability == "coding":
        output = {
            "goal": instruction,
            "artifacts": [{"id": "a1", "path": "models/res_partner.py", "intent": "edit"}],
        }
    elif capability == "repair":
        output = {"goal": instruction, "tasks": [{"id": "r1", "description": "fix"}]}
    elif capability == "execution":
        output = {
            "execution_id": f"exec-{protocol_hash}",
            "summary": "ok",
            "steps": [{"id": "s1", "action": "pytest"}],
        }
    elif capability == "context":
        return {
            "query": f"context for {module}",
            "artifacts": [],
            "metadata": {"module": module, "protocol_hash": protocol_hash},
        }
    else:
        output = {"goal": instruction}

    return {
        "instruction": instruction,
        "output": output,
        "metadata": {
            "module": module,
            "protocol_hash": protocol_hash,
            "protocol_version": "1.0",
        },
    }


class TestConversationIdentity(unittest.TestCase):
    def test_ids_deterministic(self) -> None:
        a = compute_conversation_id("sale", "hash1")
        b = compute_conversation_id("sale", "hash1")
        self.assertEqual(a, b)
        self.assertTrue(a.startswith("CONV-"))

        r1 = compute_record_id(a, 0)
        r2 = compute_record_id(a, 0)
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, compute_record_id(a, 1))
        self.assertTrue(r1.startswith("CNV-"))


class TestHistoryPolicy(unittest.TestCase):
    def test_truncate_keeps_recent_and_bounds(self) -> None:
        messages = [{"role": "user", "content": f"m{i}"} for i in range(40)]
        truncated = truncate_prefix(messages, max_messages=4, max_chars=10_000)
        self.assertEqual(len(truncated), 4)
        self.assertEqual(truncated[0]["content"], "m36")
        self.assertEqual(truncated[-1]["content"], "m39")


class TestEpisodeAndSlice(unittest.TestCase):
    def test_reconstruct_and_slice_many_replies(self) -> None:
        protocols = {
            "planner_protocol": (_row(capability="planner", module="sale", protocol_hash="p1"),),
            "coding_protocol": (_row(capability="coding", module="sale", protocol_hash="c1"),),
            "repair_protocol": (_row(capability="repair", module="sale", protocol_hash="r1"),),
            "execution_protocol": (
                _row(capability="execution", module="sale", protocol_hash="e1"),
            ),
            "context_protocol": (),
            "approval_protocol": (),
        }
        episodes = EpisodeReconstructor.reconstruct(protocols)
        self.assertEqual(len(episodes), 1)
        slices = DialogueSlicer.slice_many(episodes)
        # planner, coding, repair, execution assistant replies
        self.assertGreaterEqual(len(slices), 4)
        self.assertEqual([s.record_id for s in slices], sorted(s.record_id for s in slices))
        for item in slices:
            self.assertTrue(item.prefix)
            self.assertEqual(item.reply["role"], "assistant")
            self.assertLessEqual(len(item.prefix), MAX_HISTORY_MESSAGES)
            self.assertLessEqual(len(item.reply["content"]), MAX_MESSAGE_CHARS)

    def test_approval_not_required(self) -> None:
        protocols = {
            "planner_protocol": (_row(capability="planner", module="crm", protocol_hash="p1"),),
            "coding_protocol": (_row(capability="coding", module="crm", protocol_hash="c1"),),
            "execution_protocol": (_row(capability="execution", module="crm", protocol_hash="e1"),),
            "repair_protocol": (),
            "context_protocol": (),
            "approval_protocol": (),
        }
        episodes = EpisodeReconstructor.reconstruct(protocols)
        self.assertEqual(len(episodes), 1)
        self.assertGreaterEqual(len(DialogueSlicer.slice_many(episodes)), 2)


class TestConversationPipelineGrain(unittest.TestCase):
    def test_emits_one_record_per_assistant_reply(self) -> None:
        protocols = {
            "planner_protocol": (
                _row(capability="planner", module="m1", protocol_hash="p1", instruction="plan"),
                _row(capability="planner", module="m2", protocol_hash="p2", instruction="plan2"),
            ),
            "coding_protocol": (
                _row(capability="coding", module="m1", protocol_hash="c1", instruction="code"),
                _row(capability="coding", module="m2", protocol_hash="c2", instruction="code2"),
            ),
            "repair_protocol": (),
            "context_protocol": (),
            "execution_protocol": (
                _row(capability="execution", module="m1", protocol_hash="e1"),
                _row(capability="execution", module="m2", protocol_hash="e2"),
            ),
            "approval_protocol": (),
        }
        with tempfile.TemporaryDirectory() as tmp:
            context = PipelineContext(
                input_protocols=protocols,
                metadata=MetadataBuilder.build(
                    conversation_type=ConversationType.AGENT, source_module="sources"
                ),
                output_dir=tmp,
                source_identifier="sources",
                strict_mode=True,
            )
            result = ConversationPipeline.generate(context)
            self.assertTrue(result.success, result.diagnostics)
            jsonl = Path(tmp) / "conversation_dataset.jsonl"
            lines = [ln for ln in jsonl.read_text(encoding="utf-8").splitlines() if ln.strip()]
            self.assertGreaterEqual(len(lines), 4)
            records = [json.loads(ln) for ln in lines]
            ids = [r["record_id"] for r in records]
            self.assertEqual(ids, sorted(ids))
            self.assertEqual(len(set(ids)), len(ids))
            for rec in records:
                self.assertIn("conversation_id", rec)
                self.assertIsInstance(rec["turn_index"], int)
                projection = project_conversation(rec)
                self.assertEqual(projection.capability, "conversation")
                self.assertTrue(projection.request.turns)
                self.assertEqual(projection.response.reply.role.value, "assistant")

            # Reproducibility
            result2 = ConversationPipeline.generate(context)
            self.assertTrue(result2.success)
            self.assertEqual(
                jsonl.read_bytes(), (Path(tmp) / "conversation_dataset.jsonl").read_bytes()
            )


if __name__ == "__main__":
    unittest.main()
