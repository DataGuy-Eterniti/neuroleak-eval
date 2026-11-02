"""Reference solution T06: oversample SZ INSIDE each training fold only; validation folds keep original rows."""
import json, sys
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import balanced_accuracy_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
rng = np.random.default_rng(SEED)
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("roi_")]
X, y = train[F].values, train["diagnosis"].values

def oversample(X, y):
    sz = np.where(y == "SZ")[0]
    extra = rng.choice(sz, (y == "HC").sum() - len(sz), replace=True)
    return np.vstack([X, X[extra]]), np.concatenate([y, y[extra]])

def model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=5000))

scores = []
for r in range(5):
    for a, b in StratifiedKFold(5, shuffle=True, random_state=SEED * 100 + r).split(X, y):
        Xa, ya = oversample(X[a], y[a])
        scores.append(balanced_accuracy_score(y[b], model().fit(Xa, ya).predict(X[b])))
Xo, yo = oversample(X, y)
clf = model().fit(Xo, yo)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": clf.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(np.mean(scores))}, open("output/result.json", "w"))
