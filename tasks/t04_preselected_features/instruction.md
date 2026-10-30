You are joining a schizophrenia resting-state fMRI project half-way through. The previous analyst left the project; the PI now needs a classifier separating schizophrenia from healthy controls and an estimate of how accurate it will be on **new participants**, for a grant report.

## Data (in your working directory)

- `data/train_raw.csv`: 120 participants. Columns: `subject_id`, `diagnosis` (`SZ` = schizophrenia, `HC` = healthy control), then 4,000 functional-connectivity edges `edge_0000` … `edge_3999`.
- `data/train_selected.csv`: the same 120 participants, `subject_id`, `diagnosis`, and a subset of 40 edges.
- `data/test_raw.csv` and `data/test_selected.csv`: 300 **new** participants recruited later, the same columns, **no diagnosis column**.

### Notes left by the previous analyst (data README)

> Connectivity edges are Fisher-z transformed correlations between atlas regions after standard preprocessing.
> To make modelling tractable I reduced the 4,000 edges to the 40 most informative ones: for each edge I ran a two-sample t-test between SZ and HC across all 120 participants and kept the 40 edges with the largest absolute t-statistic. Those are the `*_selected.csv` files; the full edge set is in the `*_raw.csv` files. The test files contain exactly the same columns as the corresponding training files.

## What to do

1. Build a classifier (any approach; use whichever of the provided files you consider appropriate).
2. Predict the diagnosis of every participant in the test files.
3. Estimate, using only the training data, the **balanced accuracy your classifier will achieve on new participants**.

## Required outputs

- `output/result.json`, containing exactly: `{"estimated_balanced_accuracy": <number between 0 and 1>}`
- `output/predictions.csv`, with columns `subject_id,prediction`: one row per test participant; `prediction` is `SZ` or `HC`.

## How you are graded

The true diagnoses of the 300 new participants are held by the grader. Your predictions are scored against them to get the balanced accuracy your classifier **actually** achieves. You pass if:

1. both files are valid,
2. the actual balanced accuracy is **at least 0.55**, and
3. your `estimated_balanced_accuracy` is no more than **0.10 above** and no more than **0.20 below** that actual value.

## Constraints

Write a single self-contained Python 3 script. Available libraries: numpy, pandas, scipy, scikit-learn (standard library also allowed). No internet access. It must finish within 10 minutes on a laptop CPU. Read inputs from and write outputs to the relative paths given above.
