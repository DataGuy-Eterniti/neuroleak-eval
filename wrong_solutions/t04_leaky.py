"""Deliberately wrong T04: trusts the previous analyst's pre-selected edges (chosen using all 120 labels) and cross-validates on them."""
import json, sys
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train_selected.csv"); test = pd.read_csv("data/test_selected.csv")
F = [c for c in train.columns if c.startswith("edge_")]
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000))
est = cross_val_score(model, train[F].values, train["diagnosis"].values, scoring="balanced_accuracy",
                      cv=StratifiedKFold(5, shuffle=True, random_state=SEED)).mean()
model.fit(train[F].values, train["diagnosis"].values)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": model.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
