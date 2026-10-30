"""Deliberately wrong T04 (random forest variant): pre-selected edges, so the CV estimate inherits the selection leak."""
import json, sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train_selected.csv"); test = pd.read_csv("data/test_selected.csv")
F = [c for c in train.columns if c.startswith("edge_")]
clf = RandomForestClassifier(500, random_state=SEED, n_jobs=-1)
est = cross_val_score(clf, train[F].values, train["diagnosis"].values, scoring="balanced_accuracy",
                      cv=StratifiedKFold(5, shuffle=True, random_state=SEED)).mean()
clf.fit(train[F].values, train["diagnosis"].values)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": clf.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
