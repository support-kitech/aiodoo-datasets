"""Episode reconstruction from upstream development datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from generators.conversation.identity import compute_conversation_id
from generators.conversation.policy import MAX_MESSAGE_CHARS


@dataclass(frozen=True, slots=True)
class DialogueMessage:
    role: str
    content: str


@dataclass(frozen=True, slots=True)
class Episode:
    """One reconstructed multi-turn dialogue for a development subject."""

    conversation_id: str
    module: str
    anchor_id: str
    messages: tuple[DialogueMessage, ...]


class EpisodeReconstructor:
    """Build Planner→Coding→Repair→Execution dialogues (Context/Approval soft)."""

    @staticmethod
    def reconstruct(input_protocols: Mapping[str, Any]) -> tuple[Episode, ...]:
        coding_rows = _as_records(input_protocols.get("coding_protocol"))
        if not coding_rows:
            return ()

        by_module = {
            "planner": _index_by_module(_as_records(input_protocols.get("planner_protocol"))),
            "repair": _index_by_module(_as_records(input_protocols.get("repair_protocol"))),
            "execution": _index_by_module(_as_records(input_protocols.get("execution_protocol"))),
            "context": _index_by_module(_as_records(input_protocols.get("context_protocol"))),
            "approval": _index_by_module(_as_records(input_protocols.get("approval_protocol"))),
        }

        episodes: list[Episode] = []
        seen_ids: set[str] = set()

        for coding in sorted(coding_rows, key=_record_sort_key):
            module = _module_name(coding)
            anchor = _protocol_hash(coding) or _fallback_anchor("coding", coding)
            conversation_id = compute_conversation_id(module, anchor)
            if conversation_id in seen_ids:
                continue
            seen_ids.add(conversation_id)

            planner = _pick_related(by_module["planner"].get(module, ()), coding)
            repair = _pick_related(by_module["repair"].get(module, ()), coding)
            execution = _pick_related(by_module["execution"].get(module, ()), coding)
            context = _pick_related(by_module["context"].get(module, ()), coding)
            approval = _pick_related(by_module["approval"].get(module, ()), coding)

            messages = _build_messages(
                planner=planner,
                coding=coding,
                repair=repair,
                execution=execution,
                context=context,
                approval=approval,
            )
            if len(messages) < 2:
                continue
            if messages[-1].role != "assistant":
                continue

            episodes.append(
                Episode(
                    conversation_id=conversation_id,
                    module=module,
                    anchor_id=anchor,
                    messages=tuple(messages),
                )
            )

        episodes.sort(key=lambda e: e.conversation_id)
        return tuple(episodes)


def _as_records(raw: Any) -> tuple[Mapping[str, Any], ...]:
    if raw is None:
        return ()
    if isinstance(raw, Mapping):
        if "metadata" in raw or "output" in raw or "instruction" in raw:
            return (raw,)
        return ()
    if isinstance(raw, (list, tuple)):
        return tuple(r for r in raw if isinstance(r, Mapping))
    return ()


def _module_name(record: Mapping[str, Any]) -> str:
    meta = record.get("metadata")
    if isinstance(meta, Mapping):
        module = meta.get("module") or meta.get("source_module")
        if isinstance(module, str) and module.strip():
            return module.strip()
    return "unknown"


def _protocol_hash(record: Mapping[str, Any]) -> str:
    meta = record.get("metadata")
    if isinstance(meta, Mapping):
        value = meta.get("protocol_hash")
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _fallback_anchor(capability: str, record: Mapping[str, Any]) -> str:
    instruction = record.get("instruction")
    text = instruction.strip() if isinstance(instruction, str) else ""
    return f"{capability}:{_module_name(record)}:{text[:64]}"


def _record_sort_key(record: Mapping[str, Any]) -> tuple[str, str]:
    return (_module_name(record), _protocol_hash(record) or _fallback_anchor("row", record))


def _index_by_module(
    records: Sequence[Mapping[str, Any]],
) -> dict[str, tuple[Mapping[str, Any], ...]]:
    buckets: dict[str, list[Mapping[str, Any]]] = {}
    for record in records:
        buckets.setdefault(_module_name(record), []).append(record)
    return {module: tuple(sorted(rows, key=_record_sort_key)) for module, rows in buckets.items()}


def _pick_related(
    candidates: Sequence[Mapping[str, Any]],
    anchor: Mapping[str, Any],
) -> Mapping[str, Any] | None:
    if not candidates:
        return None
    anchor_hash = _protocol_hash(anchor)
    if anchor_hash:
        for row in candidates:
            if _protocol_hash(row) == anchor_hash:
                return row
    return candidates[0]


def _clip(text: str) -> str:
    text = " ".join(text.split())
    if len(text) <= MAX_MESSAGE_CHARS:
        return text
    return text[:MAX_MESSAGE_CHARS]


def _goal_or_instruction(record: Mapping[str, Any]) -> str:
    output = record.get("output")
    if isinstance(output, dict):
        goal = output.get("goal")
        if isinstance(goal, str) and goal.strip():
            return _clip(goal)
        summary = output.get("summary")
        if isinstance(summary, str) and summary.strip():
            return _clip(summary)
    instruction = record.get("instruction")
    if isinstance(instruction, str) and instruction.strip():
        return _clip(instruction)
    return "Continue the Odoo development task."


def _assistant_summary(capability: str, record: Mapping[str, Any]) -> str:
    output = record.get("output") if isinstance(record.get("output"), Mapping) else {}
    if capability == "planner":
        tasks = output.get("tasks") if isinstance(output, dict) else None
        count = len(tasks) if isinstance(tasks, list) else 0
        return _clip(f"Proposed a plan with {count} tasks for: {_goal_or_instruction(record)}")
    if capability == "coding":
        artifacts = output.get("artifacts") if isinstance(output, dict) else None
        count = len(artifacts) if isinstance(artifacts, list) else 0
        paths = []
        if isinstance(artifacts, list):
            for art in artifacts[:5]:
                if isinstance(art, Mapping) and art.get("path"):
                    paths.append(str(art["path"]))
        path_s = ", ".join(paths) if paths else "workspace files"
        return _clip(f"Applied {count} coding artifacts ({path_s}).")
    if capability == "repair":
        tasks = output.get("tasks") if isinstance(output, dict) else None
        count = len(tasks) if isinstance(tasks, list) else 0
        return _clip(f"Applied {count} repair task(s) for: {_goal_or_instruction(record)}")
    if capability == "execution":
        steps = output.get("steps") if isinstance(output, dict) else None
        count = len(steps) if isinstance(steps, list) else 0
        status = ""
        summary = output.get("summary") if isinstance(output, dict) else None
        if isinstance(summary, str) and summary.strip():
            status = f" Summary: {_clip(summary)}"
        return _clip(f"Executed {count} step(s).{status}")
    if capability == "context":
        query = record.get("query")
        if isinstance(query, str) and query.strip():
            return _clip(f"Retrieved context for query: {query}")
        return _clip("Retrieved relevant Odoo module context.")
    if capability == "approval":
        decision = record.get("decision")
        status = ""
        if isinstance(decision, Mapping):
            status = str(decision.get("status", ""))
        subject = record.get("subject") or record.get("subject_id") or "subject"
        return _clip(f"Approval decision for {subject}: {status or 'reviewed'}.")
    return _clip(f"Processed {capability} output.")


def _build_messages(
    *,
    planner: Mapping[str, Any] | None,
    coding: Mapping[str, Any],
    repair: Mapping[str, Any] | None,
    execution: Mapping[str, Any] | None,
    context: Mapping[str, Any] | None,
    approval: Mapping[str, Any] | None,
) -> list[DialogueMessage]:
    messages: list[DialogueMessage] = []

    if context is not None:
        messages.append(
            DialogueMessage(
                role="user",
                content=_clip(f"Gather context for module work: {_goal_or_instruction(context)}"),
            )
        )
        messages.append(
            DialogueMessage(role="assistant", content=_assistant_summary("context", context))
        )

    if planner is not None:
        messages.append(
            DialogueMessage(
                role="user",
                content=_clip(f"Create an implementation plan: {_goal_or_instruction(planner)}"),
            )
        )
        messages.append(
            DialogueMessage(role="assistant", content=_assistant_summary("planner", planner))
        )

    messages.append(
        DialogueMessage(
            role="user",
            content=_clip(f"Implement the required changes: {_goal_or_instruction(coding)}"),
        )
    )
    messages.append(DialogueMessage(role="assistant", content=_assistant_summary("coding", coding)))

    if repair is not None:
        messages.append(
            DialogueMessage(
                role="user",
                content=_clip(f"Repair the failing behavior: {_goal_or_instruction(repair)}"),
            )
        )
        messages.append(
            DialogueMessage(role="assistant", content=_assistant_summary("repair", repair))
        )

    if execution is not None:
        messages.append(
            DialogueMessage(
                role="user",
                content=_clip(f"Execute and validate: {_goal_or_instruction(execution)}"),
            )
        )
        messages.append(
            DialogueMessage(role="assistant", content=_assistant_summary("execution", execution))
        )

    if approval is not None:
        messages.append(
            DialogueMessage(
                role="user",
                content=_clip("Review the development subject and decide approval status."),
            )
        )
        messages.append(
            DialogueMessage(role="assistant", content=_assistant_summary("approval", approval))
        )

    return messages
