"""Deliberately wrong T01: selects the top-50 features on ALL subjects, then cross-validates."""
import json, sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold, cross_val_score

SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
train = pd.read_csv("data/train.csv"); test = pd.read_csv("data/test.csv")
X = train.filter(like="fc_").values; y = train["diagnosis"].values
sc = StandardScaler().fit(X); sel = SelectKBest(f_classif, k=50).fit(sc.transform(X), y)
Xs = sel.transform(sc.transform(X))
clf = LinearSVC(C=1.0, max_iter=20000)
est = cross_val_score(clf, Xs, y, cv=StratifiedKFold(5, shuffle=True, random_state=SEED), scoring="balanced_accuracy").mean()
clf.fit(Xs, y)
pred = clf.predict(sel.transform(sc.transform(test.filter(like="fc_").values)))
pd.DataFrame({"subject_id": test["subject_id"], "prediction": pred}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": float(est)}, open("output/result.json", "w"))
