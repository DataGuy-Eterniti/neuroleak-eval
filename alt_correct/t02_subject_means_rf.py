"""Alternative correct T02: average slices per subject, random forest, single subject-level 5-fold CV."""
import json, sys
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("feat_")]
agg = train.groupby("subject_id").agg({**{f: "mean" for f in F}, "diagnosis": "first"})
clf = RandomForestClassifier(500, random_state=SEED, n_jobs=-1)
est = cross_val_score(clf, agg[F].values, agg["diagnosis"].values, cv=StratifiedKFold(5, shuffle=True, random_state=SEED), scoring="balanced_accuracy").mean()
clf.fit(agg[F].values, agg["diagnosis"].values)
tagg = test.groupby("subject_id")[F].mean()
pd.DataFrame({"subject_id": tagg.index, "prediction": clf.predict(tagg.values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
