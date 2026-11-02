"""Reference solution T05: drop treatment variables (they cannot exist at first contact); MRI + demographics only."""
import json, sys
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
F = [c for c in train.columns if c.startswith("roi_")] + ["age", "years_education"]
model = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=5000))
est = cross_val_score(model, train[F].values, train["diagnosis"].values, scoring="balanced_accuracy",
                      cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEED)).mean()
model.fit(train[F].values, train["diagnosis"].values)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": model.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
