"""Grader validation: does the grader accept correct answers and reject wrong ones?

Runs, against each task's real eval data:
  * the reference solution and alternative correct solutions (must PASS),
  * deliberately wrong / leaky / gaming solutions (must FAIL),
each with several CV random seeds, and reports false-fail and false-pass
counts. No API key needed. Writes results/grader_validation.csv and .md.

    python validate_graders.py            # 5 seeds per solution
    python validate_graders.py --seeds 10
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd

from evalkit.grader import grade
from evalkit.sandbox import build_workspace, run_script

ROOT = Path(__file__).parent
CASES = {
    "t01_feature_selection_leakage": {
        "PASS": ["reference/t01_solve.py", "alt_correct/t01_logreg_single_cv.py"],
        "FAIL": ["wrong_solutions/t01_leaky.py", "wrong_solutions/overclaim_constant.py",
                 "wrong_solutions/broken_outputs.py"],
    },
    "t02_slice_level_leakage": {
        "PASS": ["reference/t02_solve.py", "alt_correct/t02_subject_means_rf.py"],
        "FAIL": ["wrong_solutions/t02_leaky.py", "wrong_solutions/t02_leaky_linear.py",
                 "wrong_solutions/overclaim_constant.py", "wrong_solutions/honest_constant.py",
                 "wrong_solutions/broken_outputs.py"],
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=5)
    a = ap.parse_args()
    rows = []
    for task, groups in CASES.items():
        for expected, sols in groups.items():
            for sol in sols:
                for seed in range(a.seeds):
                    ws, hidden = build_workspace(task)
                    r = run_script((ROOT / sol).read_text(), ws, args=[str(seed)])
                    g = grade(task, ws, hidden)
                    shutil.rmtree(ws, ignore_errors=True)
                    got = "PASS" if g["pass"] else "FAIL"
                    rows.append({"task": task, "solution": sol, "seed": seed, "expected": expected,
                                 "got": got, "estimate": g["estimate"], "actual": g["actual"],
                                 "gap": g["gap"], "error": g["error"] or (r["stderr"][-200:] if r["returncode"] else None)})
                    print(f"{task[:3]} {sol:45s} seed={seed} expected={expected} got={got} gap={g['gap']}")
    df = pd.DataFrame(rows)
    Path(ROOT / "results").mkdir(exist_ok=True)
    df.to_csv(ROOT / "results/grader_validation.csv", index=False)
    summ = (df.assign(correct=df.expected == df.got)
              .groupby(["task", "solution", "expected"])
              .agg(runs=("correct", "size"), agree=("correct", "sum"),
                   mean_gap=("gap", "mean"), min_gap=("gap", "min"), max_gap=("gap", "max"))
              .reset_index())
    ff = int(((df.expected == "PASS") & (df.got == "FAIL")).sum())
    fp = int(((df.expected == "FAIL") & (df.got == "PASS")).sum())
    md = ["# Grader validation", "", f"False fails: **{ff}** / {int((df.expected=='PASS').sum())} correct runs  ",
          f"False passes: **{fp}** / {int((df.expected=='FAIL').sum())} wrong runs", "",
          summ.round(3).to_markdown(index=False)]
    (ROOT / "results/grader_validation.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
