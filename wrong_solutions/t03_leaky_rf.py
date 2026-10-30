"""Deliberately wrong T03 (random forest variant): scan-level CV, repeat scans leak across folds."""
import json, sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("roi_")]
clf = RandomForestClassifier(300, random_state=SEED, n_jobs=-1)
est = cross_val_score(clf, train[F].values, train["diagnosis"].values, scoring="balanced_accuracy",
                      cv=StratifiedKFold(5, shuffle=True, random_state=SEED)).mean()
clf.fit(train[F].values, train["diagnosis"].values)
pd.DataFrame({"scan_id": test["scan_id"], "prediction": clf.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
