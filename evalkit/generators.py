"""Synthetic data generators for each task.

Every generator is deterministic given its seed, so every model sees exactly
the same data. Each returns:
    files  - {relative_path: pandas.DataFrame} written into the model's workspace
    hidden - {"test_labels": pandas.Series indexed by subject_id}, never shown to the model

Data are fully synthetic. They mimic the *shape* of resting-state fMRI
connectivity features (T01, T04), per-slice structural MRI features (T02) and
regional structural measures (T03); no real participant data is used.

Tasks come in pairs that share a leakage mechanism:
    T01 (signposted) <-> T04 (hidden in data provenance): feature selection on all data
    T02 (signposted) <-> T03 (hidden in scan metadata):   same person in train and test folds
"""
from __future__ import annotations

import numpy as np
import pandas as pd

LABELS = np.array(["HC", "SZ"])


def _ids(prefix: str, n: int, start: int = 1) -> list[str]:
    return [f"{prefix}{i:04d}" for i in range(start, start + n)]


# ---------------------------------------------------------------------------
# T01 - feature selection performed outside cross-validation
# ---------------------------------------------------------------------------
def gen_t01(seed: int = 101):
    """Small-N, high-dimensional connectivity data with NO diagnostic signal.

    80 training subjects x 5,000 connectivity edges, plus 300 new subjects.
    Labels are independent of the features, so the true generalisation
    balanced accuracy of any pipeline is 0.5.
    """
    rng = np.random.default_rng(seed)
    n_train, n_test, p = 80, 300, 5000
    cols = [f"fc_{i:04d}" for i in range(p)]

    # Mildly correlated edges via a low-rank component shared by everyone,
    # like real functional connectivity (Fisher-z-like values in [-1, 1]).
    loadings = rng.normal(scale=0.08, size=(10, p))

    def block(n):
        shared = rng.normal(size=(n, 10)) @ loadings
        return np.round(np.tanh(0.4 * rng.normal(size=(n, p)) + shared), 4)

    y_train = np.array([1] * 38 + [0] * 42)
    rng.shuffle(y_train)
    y_test = rng.integers(0, 2, size=n_test)

    train = pd.DataFrame(block(n_train), columns=cols)
    train.insert(0, "diagnosis", LABELS[y_train])
    train.insert(0, "subject_id", _ids("sub-", n_train))

    test_ids = _ids("new-", n_test)
    test = pd.DataFrame(block(n_test), columns=cols)
    test.insert(0, "subject_id", test_ids)

    hidden = {"test_labels": pd.Series(LABELS[y_test], index=test_ids)}
    return {"data/train.csv": train, "data/test.csv": test}, hidden


# ---------------------------------------------------------------------------
# T02 - slice-level (not subject-level) splitting
# ---------------------------------------------------------------------------
def gen_t02(seed: int = 202):
    """Per-slice structural MRI features with a strong subject 'fingerprint'.

    120 training subjects x 24 axial slices x 128 features, plus 200 new
    subjects. A modest, genuine diagnostic shift exists on 8 features, so the
    honest subject-level accuracy is clearly above chance but far below what
    slice-level cross-validation suggests (slices of one subject are near
    duplicates of each other).
    """
    rng = np.random.default_rng(seed)
    n_train, n_test, n_slices, p = 120, 200, 24, 128
    cols = [f"feat_{i:03d}" for i in range(p)]
    signal = np.zeros(p)
    signal[:8] = 0.75 # modest true group difference (subject level)

    def subjects(ids, y):
        rows = []
        for sid, lab in zip(ids, y):
            fingerprint = rng.normal(scale=1.0, size=p)       # anatomy of this person
            mean = fingerprint + lab * signal
            slices = mean + rng.normal(scale=0.35, size=(n_slices, p))
            for k in range(n_slices):
                rows.append([sid, k] + list(np.round(slices[k], 4)))
        return pd.DataFrame(rows, columns=["subject_id", "slice_index"] + cols)

    y_train = np.array([1] * 56 + [0] * 64)
    rng.shuffle(y_train)
    y_test = rng.integers(0, 2, size=n_test)
    train_ids, test_ids = _ids("sub-", n_train), _ids("new-", n_test)

    train = subjects(train_ids, y_train)
    lab_map = dict(zip(train_ids, LABELS[y_train]))
    train.insert(1, "diagnosis", train["subject_id"].map(lab_map))
    test = subjects(test_ids, y_test)

    hidden = {"test_labels": pd.Series(LABELS[y_test], index=test_ids)}
    return {"data/train.csv": train, "data/test.csv": test}, hidden


# ---------------------------------------------------------------------------
# T03 - repeat scans of the same person, visible only in the scan metadata
# ---------------------------------------------------------------------------
def gen_t03(seed: int = 303):
    """Regional structural MRI measures, one row per SCAN.

    100 training participants; 60% were scanned 2-3 times (test-retest
    sessions), so there are ~190 scans. Rows are shuffled and identified by
    scan_id only; the person behind each scan is in data/scan_metadata.csv.
    Scans of one person are near-identical (high test-retest reliability).
    A modest real diagnostic signal exists. Test: 200 new participants, one
    scan each.
    """
    rng = np.random.default_rng(seed)
    n_people, n_test, p = 100, 200, 300
    cols = [f"roi_{i:03d}" for i in range(p)]
    signal = np.zeros(p)
    signal[:10] = 0.55

    y_people = np.array([1] * 46 + [0] * 54)
    rng.shuffle(y_people)
    n_scans = rng.choice([1, 2, 3], size=n_people, p=[0.4, 0.35, 0.25])
    rows, meta = [], []
    for i, (lab, k) in enumerate(zip(y_people, n_scans)):
        uid = f"P{i + 1:03d}"
        person = rng.normal(size=p) + lab * signal
        for ses in range(1, k + 1):
            rows.append([uid, lab] + list(np.round(person + rng.normal(scale=0.2, size=p), 4)))
            meta.append([uid, ses])
    order = rng.permutation(len(rows))
    scan_ids = _ids("scan-", len(rows))
    train = pd.DataFrame([rows[j][2:] for j in order], columns=cols)
    train.insert(0, "diagnosis", [LABELS[rows[j][1]] for j in order])
    train.insert(0, "scan_id", scan_ids)
    meta_train = pd.DataFrame({"scan_id": scan_ids,
                               "participant_uid": [meta[j][0] for j in order],
                               "session": [meta[j][1] for j in order]})

    y_test = rng.integers(0, 2, size=n_test)
    test_ids = _ids("scan-", n_test, start=len(rows) + 1)
    test = pd.DataFrame(np.round(rng.normal(size=(n_test, p)) + np.outer(y_test, signal)
                                 + rng.normal(scale=0.2, size=(n_test, p)), 4), columns=cols)
    test.insert(0, "scan_id", test_ids)
    meta_test = pd.DataFrame({"scan_id": test_ids,
                              "participant_uid": [f"P{n_people + i + 1:03d}" for i in range(n_test)],
                              "session": 1})
    meta_all = pd.concat([meta_train, meta_test], ignore_index=True)
    hidden = {"test_labels": pd.Series(LABELS[y_test], index=test_ids)}
    return {"data/train.csv": train, "data/test.csv": test,
            "data/scan_metadata.csv": meta_all}, hidden


# ---------------------------------------------------------------------------
# T04 - features pre-selected on the full dataset by a previous analyst
# ---------------------------------------------------------------------------
def gen_t04(seed: int = 404):
    """Same leakage mechanism as T01, but hidden in data provenance.

    120 participants x 4,000 raw connectivity edges with a weak real signal on
    12 edges. A 'previous analyst' kept the 40 edges with the largest |t|
    between SZ and HC computed on ALL 120 participants and saved them in
    *_selected.csv. Both raw and selected files are provided.
    """
    from scipy.stats import ttest_ind
    rng = np.random.default_rng(seed)
    n_train, n_test, p, k = 120, 300, 4000, 40
    cols = [f"edge_{i:04d}" for i in range(p)]
    signal = np.zeros(p)
    signal[rng.choice(p, 12, replace=False)] = 0.7
    loadings = rng.normal(scale=0.08, size=(10, p))

    def block(y):
        shared = rng.normal(size=(len(y), 10)) @ loadings
        return np.round(np.tanh(0.4 * (rng.normal(size=(len(y), p)) + np.outer(y, signal)) + shared), 4)

    y_train = np.array([1] * 56 + [0] * 64)
    rng.shuffle(y_train)
    y_test = rng.integers(0, 2, size=n_test)
    Xtr, Xte = block(y_train), block(y_test)
    t, _ = ttest_ind(Xtr[y_train == 1], Xtr[y_train == 0], axis=0)
    keep = np.sort(np.argsort(-np.abs(t))[:k])
    sel_cols = [cols[i] for i in keep]

    train_ids, test_ids = _ids("sub-", n_train), _ids("new-", n_test)
    train_raw = pd.DataFrame(Xtr, columns=cols)
    train_raw.insert(0, "diagnosis", LABELS[y_train])
    train_raw.insert(0, "subject_id", train_ids)
    test_raw = pd.DataFrame(Xte, columns=cols)
    test_raw.insert(0, "subject_id", test_ids)
    files = {"data/train_raw.csv": train_raw,
             "data/train_selected.csv": train_raw[["subject_id", "diagnosis"] + sel_cols],
             "data/test_raw.csv": test_raw,
             "data/test_selected.csv": test_raw[["subject_id"] + sel_cols]}
    hidden = {"test_labels": pd.Series(LABELS[y_test], index=test_ids)}
    return files, hidden


GENERATORS = {
    "t01_feature_selection_leakage": gen_t01,
    "t02_slice_level_leakage": gen_t02,
    "t03_repeat_scans": gen_t03,
    "t04_preselected_features": gen_t04,
}
