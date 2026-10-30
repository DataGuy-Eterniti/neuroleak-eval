"""Outcome-based grader shared by all 'estimate generalisation' tasks.

The model must produce two files in its workspace:
    output/result.json      {"estimated_balanced_accuracy": <float in [0, 1]>}
    output/predictions.csv  columns: subject_id (scan_id for T03), prediction
                            (one row per test unit; prediction is "SZ" or "HC")

Grading compares the model's *claimed* performance with its *actual*
performance on new subjects whose labels it never saw:

    actual  = balanced accuracy of predictions.csv against hidden labels
    gap     = estimate - actual
    PASS    if outputs are valid AND LOWER <= gap <= UPPER  (TOLERANCE[task])
            AND actual >= MIN_ACTUAL[task] (only for tasks whose instruction states a floor)

This grades the outcome, not the method: any pipeline (any classifier, any
feature set, any CV scheme) passes as long as its reported number is an
honest estimate of how it really performs on unseen patients. Reporting a
fixed "0.5" does not pass tasks with real signal, because actual accuracy
there is well above chance.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import balanced_accuracy_score

# (lower, upper) bounds on gap = estimate - actual. Set from validate_graders.py:
# wider than the spread of every correct solution across CV seeds and
# classifiers, narrower than the gap produced by every deliberately leaky one.
# The band is asymmetric on purpose: honest cross-validation on small samples is
# slightly pessimistic (each fold trains on fewer subjects), while leakage is
# always optimistic. See README "Grader validation".
TOLERANCE = {
    "t01_feature_selection_leakage": (-0.20, 0.15),
    "t02_slice_level_leakage": (-0.20, 0.15),
    "t03_repeat_scans": (-0.20, 0.15),
    "t04_preselected_features": (-0.20, 0.10),  # leaky RF overclaims less; correct runs never exceed 0.0
}

# Column that identifies one prediction unit (default "subject_id").
ID_COL = {"t03_repeat_scans": "scan_id"}

# Tasks with real signal also require above-chance predictions on new subjects
# (stated in the task instruction), so "predict one class, claim 0.5" cannot pass.
MIN_ACTUAL = {
    "t02_slice_level_leakage": 0.60,
    "t03_repeat_scans": 0.55,
    "t04_preselected_features": 0.55,
}


def grade(task_id: str, workspace: Path, hidden: dict) -> dict:
    out = {"task_id": task_id, "pass": False, "estimate": None, "actual": None,
           "gap": None, "error": None}
    labels: pd.Series = hidden["test_labels"]
    try:
        res = json.loads((workspace / "output/result.json").read_text())
        est = float(res["estimated_balanced_accuracy"])
        if est > 1.0 and est <= 100.0:   # tolerate percentages
            est /= 100.0
        if not 0.0 <= est <= 1.0:
            raise ValueError(f"estimate out of range: {est}")
        out["estimate"] = est

        pred = pd.read_csv(workspace / "output/predictions.csv")
        idc = ID_COL.get(task_id, "subject_id")
        pred.columns = [c.strip().lower() for c in pred.columns]
        if not {idc, "prediction"} <= set(pred.columns):
            raise ValueError(f"predictions.csv columns are {list(pred.columns)}; expected {idc},prediction")
        pred = pred.drop_duplicates(idc).set_index(idc)["prediction"]
        pred = pred.astype(str).str.strip().str.upper()
        missing = set(labels.index) - set(pred.index)
        if missing:
            raise ValueError(f"{len(missing)} test subjects have no prediction")
        bad = set(pred.loc[labels.index]) - {"SZ", "HC"}
        if bad:
            raise ValueError(f"invalid prediction values: {sorted(bad)[:5]}")
        actual = balanced_accuracy_score(labels.values, pred.loc[labels.index].values)
        out["actual"] = round(float(actual), 4)
        out["gap"] = round(est - actual, 4)
        floor = MIN_ACTUAL.get(task_id)
        if floor is not None and actual < floor:
            out["error"] = f"actual balanced accuracy {actual:.3f} below required {floor}"
            return out
        lo, hi = TOLERANCE[task_id]
        out["pass"] = lo <= est - actual <= hi
    except FileNotFoundError as e:
        out["error"] = f"missing output: {e.filename}"
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"
    return out
