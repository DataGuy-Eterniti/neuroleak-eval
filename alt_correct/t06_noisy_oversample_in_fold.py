"""Alternative correct T06: jittered synthetic SZ records created inside each training fold, single 5-fold CV."""
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
    synth = X[extra] + 0.1 * X.std(axis=0) * rng.normal(size=(len(extra), X.shape[1]))
    return np.vstack([X, synth]), np.concatenate([y, y[extra]])

def model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.05, max_iter=5000))

scores = []
for a, b in StratifiedKFold(5, shuffle=True, random_state=SEED).split(X, y):
    Xa, ya = oversample(X[a], y[a])
    scores.append(balanced_accuracy_score(y[b], model().fit(Xa, ya).predict(X[b])))
clf = model().fit(*oversample(X, y))
pd.DataFrame({"subject_id": test["subject_id"], "prediction": clf.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(np.mean(scores))}, open("output/result.json", "w"))
