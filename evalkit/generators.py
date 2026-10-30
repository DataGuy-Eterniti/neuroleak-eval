"""Synthetic data generators for each task.

Every generator is deterministic given its seed, so every model sees exactly
the same data. Each returns:
    files  - {relative_path: pandas.DataFrame} written into the model's workspace
    hidden - {"test_labels": pandas.Series indexed by subject_id}, never shown to the model

Data are fully synthetic. They mimic the *shape* of resting-state fMRI
connectivity features (T01) and per-slice structural MRI features (T02);
no real participant data is used.
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


GENERATORS = {
    "t01_feature_selection_leakage": gen_t01,
    "t02_slice_level_leakage": gen_t02,
}
