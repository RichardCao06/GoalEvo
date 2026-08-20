import json
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "taxonomy_cases"


def test_candidate_taxonomy_is_balanced_and_not_gold() -> None:
    records = [
        json.loads(line)
        for path in sorted((TAXONOMY / "candidates").glob("*.jsonl"))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert len(records) == 72
    counts = Counter(record["proposed_label"] for record in records)
    assert set(counts.values()) == {12}
    assert all(record["gold_status"] == "not_gold" for record in records)


def test_human_review_batch_does_not_leak_proposed_labels() -> None:
    batch = yaml.safe_load((TAXONOMY / "human_review_batch_01.yaml").read_text(encoding="utf-8"))
    assert len(batch["cases"]) == 24
    assert all("proposed_label" not in case for case in batch["cases"])
    assert all(case["coder_label"] == "" for case in batch["cases"])
