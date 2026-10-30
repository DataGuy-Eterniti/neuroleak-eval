"""Reference solution T03: map scans to people via scan_metadata.csv and group CV folds by person."""
import json, sys
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedGroupKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
meta = pd.read_csv("data/scan_metadata.csv").set_index("scan_id")
F = [c for c in train.columns if c.startswith("roi_")]
X, y = train[F].values, train["diagnosis"].values
groups = train["scan_id"].map(meta["participant_uid"]).values
model = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, max_iter=5000))
scores = [cross_val_score(model, X, y, groups=groups, scoring="balanced_accuracy",
                          cv=StratifiedGroupKFold(5, shuffle=True, random_state=SEED * 100 + r)).mean()
          for r in range(5)]
model.fit(X, y)
pd.DataFrame({"scan_id": test["scan_id"], "prediction": model.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(np.mean(scores))}, open("output/result.json", "w"))
