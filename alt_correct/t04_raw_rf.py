"""Alternative correct T04: raw edges, selection inside the pipeline, random forest, single 5-fold CV."""
import json, sys
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train_raw.csv"); test = pd.read_csv("data/test_raw.csv")
F = [c for c in train.columns if c.startswith("edge_")]
pipe = make_pipeline(SelectKBest(f_classif, k=40), RandomForestClassifier(500, random_state=SEED, n_jobs=-1))
est = cross_val_score(pipe, train[F].values, train["diagnosis"].values, scoring="balanced_accuracy",
                      cv=StratifiedKFold(5, shuffle=True, random_state=SEED)).mean()
pipe.fit(train[F].values, train["diagnosis"].values)
pd.DataFrame({"subject_id": test["subject_id"], "prediction": pipe.predict(test[F].values)}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
