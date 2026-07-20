"""Tests for generators.common.contract.eval_corpus."""

from __future__ import annotations

import json

import pytest

from generators.common.contract.adapters import ContractAdapterError
from generators.common.contract.eval_corpus import build_eval_corpus, write_eval_corpus

_VALID_PLANNER_RECORD = {
    "instruction": "Build feature X",
    "input": "ctx",
    "output": {
        "goal": "Build feature X",
        "tasks": [{"id": "t1", "title": "Create model"}],
    },
    "metadata": {"module": "my_module", "protocol_hash": "abc123"},
}

_INVALID_PLANNER_RECORD = {"instruction": "no output here", "metadata": {"module": "m"}}


class TestBuildEvalCorpus:
    def test_unsupported_capability_raises(self) -> None:
        with pytest.raises(ContractAdapterError):
            build_eval_corpus("not-a-capability", [])

    def test_all_valid_records_are_written(self) -> None:
        records = [_VALID_PLANNER_RECORD for _ in range(3)]
        report = build_eval_corpus("planner", records, sample_size=10)
        assert report.candidates == 3
        assert report.projected == 3
        assert report.skipped_projection == 0
        assert report.written == 3
        for case in report.cases:
            assert case["capability"] == "planner"
            assert case["request"]["capability"] == "planner"
            assert case["expected_response"]["capability"] == "planner"
            assert case["source_protocol_hash"] == "abc123"

    def test_unprojectable_records_are_skipped_and_counted(self) -> None:
        records = [_VALID_PLANNER_RECORD, _INVALID_PLANNER_RECORD]
        report = build_eval_corpus("planner", records, sample_size=10)
        assert report.candidates == 2
        assert report.projected == 1
        assert report.skipped_projection == 1
        assert report.written == 1

    def test_empty_input_produces_empty_report(self) -> None:
        report = build_eval_corpus("planner", [], sample_size=10)
        assert report.candidates == 0
        assert report.written == 0

    def test_sample_size_is_respected(self) -> None:
        records = [_VALID_PLANNER_RECORD for _ in range(5)]
        report = build_eval_corpus("planner", records, sample_size=2)
        assert report.candidates == 2
        assert report.written == 2

    def test_sampling_is_deterministic(self) -> None:
        records = [
            {**_VALID_PLANNER_RECORD, "metadata": {"module": "m", "protocol_hash": str(i)}}
            for i in range(5)
        ]
        report_a = build_eval_corpus("planner", records, sample_size=3)
        report_b = build_eval_corpus("planner", list(reversed(records)), sample_size=3)
        hashes_a = [case["source_protocol_hash"] for case in report_a.cases]
        hashes_b = [case["source_protocol_hash"] for case in report_b.cases]
        assert hashes_a == hashes_b


class TestWriteEvalCorpus:
    def test_writes_jsonl_manifest_and_statistics(self, tmp_path) -> None:  # type: ignore[no-untyped-def]
        records = [_VALID_PLANNER_RECORD for _ in range(2)]
        report = write_eval_corpus("planner", records, tmp_path, sample_size=10)
        assert report.written == 2

        jsonl_path = tmp_path / "planner_eval_corpus.jsonl"
        manifest_path = tmp_path / "planner_eval_corpus_manifest.json"
        statistics_path = tmp_path / "planner_eval_corpus_statistics.json"
        assert jsonl_path.exists()
        assert manifest_path.exists()
        assert statistics_path.exists()

        lines = jsonl_path.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        for line in lines:
            case = json.loads(line)
            assert case["capability"] == "planner"

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["row_count"] == 2
