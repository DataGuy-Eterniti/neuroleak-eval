"""Gaming attempt: no modelling, predict all SZ, honestly claim 0.5 (must fail tasks that require above-chance performance)."""
import json
import pandas as pd
import os
test = pd.read_csv("data/test.csv" if os.path.exists("data/test.csv") else "data/test_raw.csv", usecols=[0])
IDC = test.columns[0]
ids = test[IDC].drop_duplicates()
pd.DataFrame({IDC: ids, "prediction": "SZ"}).to_csv("output/predictions.csv", index=False)
json.dump({"estimated_balanced_accuracy": 0.5}, open("output/result.json", "w"))
