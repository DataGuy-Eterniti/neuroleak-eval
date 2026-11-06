"""Rebuild results/runs.jsonl from the saved transcripts.

Each transcript (transcripts/<model>/<task>/trial_<k>.json) holds the full
prompt, model reply, executed code, execution log AND the grade record of one
trial. Rebuilding runs.jsonl from them guarantees that every reported score
has its raw output in the repository (one row per transcript, nothing else).

Why this exists: on 5 Nov 2026 the full run was accidentally launched three
times in parallel. All three processes appended to runs.jsonl, but each
transcript file was overwritten by the last process to reach it, so rows and
transcripts no longer matched. The rows without a surviving transcript were
discarded; the reported results are exactly the runs whose raw outputs are
included. See README, "Run log and integrity note".

    python tools/rebuild_runs_from_transcripts.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paths = sorted((ROOT / "transcripts").glob("*/*/trial_*.json"))
rows = []
for p in paths:
    rec = json.loads(p.read_text())["record"]
    rec["transcript"] = str(p.relative_to(ROOT))
    rows.append(rec)
rows.sort(key=lambda r: (r["model"], r["task"], r["trial"]))
(ROOT / "results/runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
print(f"rebuilt results/runs.jsonl from {len(rows)} transcripts")
