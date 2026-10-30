"""Alternative correct T01: different classifier and a single 5-fold CV (selection still inside folds)."""
import json, sys
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
X = train.filter(like="fc_").values; y = train["diagnosis"].values
pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif, k=50), LogisticRegression(max_iter=5000))
est = cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=SEED), scoring="balanced_accuracy").mean()
pipe.fit(X, y)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": pipe.predict(test.filter(like="fc_").values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
