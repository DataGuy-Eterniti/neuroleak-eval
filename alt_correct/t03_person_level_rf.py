"""Alternative correct T03: average each person's scans, random forest, person-level 5-fold CV."""
import json, sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
meta = pd.read_csv("data/scan_metadata.csv").set_index("scan_id")
F = [c for c in train.columns if c.startswith("roi_")]
train["uid"] = train["scan_id"].map(meta["participant_uid"])
people = train.groupby("uid").agg({**{f: "mean" for f in F}, "diagnosis": "first"})
clf = RandomForestClassifier(500, random_state=SEED, n_jobs=-1)
est = cross_val_score(clf, people[F].values, people["diagnosis"].values, scoring="balanced_accuracy",
                      cv=StratifiedKFold(5, shuffle=True, random_state=SEED)).mean()
clf.fit(people[F].values, people["diagnosis"].values)
pd.DataFrame({"scan_id": test["scan_id"], "prediction": clf.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
