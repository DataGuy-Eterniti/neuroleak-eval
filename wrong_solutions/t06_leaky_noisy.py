"""Deliberately wrong T06 (synthetic variant): jittered SZ copies created BEFORE cross-validation."""
import json, sys
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
rng = np.random.default_rng(SEED)
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("roi_")]
X, y = train[F].values, train["diagnosis"].values
sz = np.where(y == "SZ")[0]
extra = rng.choice(sz, (y == "HC").sum() - len(sz), replace=True)
synth = X[extra] + 0.1 * X.std(axis=0) * rng.normal(size=(len(extra), X.shape[1]))
Xo, yo = np.vstack([X, synth]), np.concatenate([y, y[extra]])
model = make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=5000))
est = cross_val_score(model, Xo, yo, scoring="balanced_accuracy", cv=StratifiedKFold(5, shuffle=True, random_state=SEED)).mean()
model.fit(Xo, yo)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": model.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
