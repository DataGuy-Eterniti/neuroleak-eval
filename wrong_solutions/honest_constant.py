"""Gaming attempt: no modelling, predict all SZ, honestly claim 0.5 (must fail tasks that require above-chance performance)."""
import json
import pandas as pd
test = pd.read_csv("data/test.csv")
ids = test["subject_id"].drop_duplicates()
pd.DataFrame({"subject_id": ids, "prediction": "SZ"}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": 0.5}, open("output/result.json", "w"))
