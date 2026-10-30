"""Reference solution T02: subject-grouped CV (5x5), slice model, subject-level vote."""
import json, sys
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import balanced_accuracy_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("feat_")]
X, y, g = train[F].values, train["diagnosis"].values, train["subject_id"].values

def model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=5000))

def subject_vote(clf, df):
    p = clf.predict_proba(df[F].values)[:, list(clf.classes_).index("SZ")]
    m = pd.Series(p, index=df["subject_id"].values).groupby(level=0).mean()
    return pd.Series(np.where(m >= 0.5, "SZ", "HC"), index=m.index)

scores = []
splits = [sp for r in range(5) for sp in StratifiedGroupKFold(5, shuffle=True, random_state=SEED * 100 + r).split(X, y, g)]
for tr, te in splits:
    clf = model().fit(X[tr], y[tr])
    pred = subject_vote(clf, train.iloc[te])
    truth = train.iloc[te].groupby("subject_id")["diagnosis"].first().loc[pred.index]
    scores.append(balanced_accuracy_score(truth, pred))
clf = model().fit(X, y)
pred = subject_vote(clf, test)
pd.DataFrame({"subject_id": pred.index, "prediction": pred.values}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(np.mean(scores))}, open("output/result.json", "w"))
