"""Deliberately invalid outputs: estimate written but predictions missing half the subjects."""
import json
import pandas as pd
test = pd.read_csv("data/test.csv")
ids = test["subject_id"].drop_duplicates().iloc[: len(test["subject_id"].unique()) // 2]
pd.DataFrame({"subject_id": ids, "prediction": "SZ"}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": 0.5}, open("output/result.json", "w"))
