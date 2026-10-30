"""Reference solution T01: feature selection INSIDE each CV fold (Pipeline)."""
import json, sys
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.svm import LinearSVC
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
X = train.filter(like="fc_").values; y = train["diagnosis"].values
pipe = make_pipeline(StandardScaler(), SelectKBest(f_classif, k=50), LinearSVC(C=1.0, max_iter=20000))
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=SEED)
est = cross_val_score(pipe, X, y, cv=cv, scoring="balanced_accuracy").mean()
pipe.fit(X, y)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": pipe.predict(test.filter(like="fc_").values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
