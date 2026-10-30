"""Deliberately wrong T02: random K-fold over SLICES, so each subject's slices sit in train and test."""
import json, sys
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("feat_")]
X, y = train[F].values, train["diagnosis"].values
clf = RandomForestClassifier(300, random_state=SEED, n_jobs=-1)
est = cross_val_score(clf, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=SEED), scoring="balanced_accuracy").mean()
clf.fit(X, y)
p = clf.predict_proba(test[F].values)[:, list(clf.classes_).index("SZ")]
m = pd.Series(p, index=test["subject_id"].values).groupby(level=0).mean()
pd.DataFrame({"subject_id": m.index, "prediction": np.where(m >= 0.5, "SZ", "HC")}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
