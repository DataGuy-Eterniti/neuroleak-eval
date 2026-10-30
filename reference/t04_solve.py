"""Reference solution T04: ignore the leaked *_selected files; redo selection INSIDE each CV fold on the raw edges."""
import json, sys
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train_raw.csv"); test = pd.read_csv("data/test_raw.csv")
F = [c for c in train.columns if c.startswith("edge_")]
X, y = train[F].values, train["diagnosis"].values
pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif, k=40), LogisticRegression(max_iter=5000))
est = cross_val_score(pipe, X, y, scoring="balanced_accuracy",
                      cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEED)).mean()
pipe.fit(X, y)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": pipe.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
