You are the data scientist for a schizophrenia imaging study. The clinical team wants a classifier that distinguishes schizophrenia from healthy controls using regional brain measures from T1-weighted MRI, and needs to know how accurate it will be on **new participants**.

## Data (in your working directory)

- `data/train.csv`: one row per **scan**, in no particular order. Columns: `scan_id`, `diagnosis` (`SZ` = schizophrenia, `HC` = healthy control), then 300 regional measures `roi_000` … `roi_299` (cortical thickness and subcortical volumes, already in standard units).
- `data/test.csv`: scans from participants recruited later, same measures, **no diagnosis column**.
- `data/scan_metadata.csv`: scan-level metadata for every scan in both files.

### Data dictionary (from the study's data manager)

| File | Column | Meaning |
|---|---|---|
| scan_metadata.csv | `scan_id` | Unique identifier of one MRI acquisition. Matches `scan_id` in train.csv and test.csv. |
| scan_metadata.csv | `participant_uid` | Pseudonymised identifier of the person scanned. |
| scan_metadata.csv | `session` | Visit number for that person (1 = baseline; the study protocol included optional follow-up visits). |

## What to do

1. Train a classifier on `data/train.csv` (you may use any approach and any of the provided files).
2. Predict the diagnosis for every scan in `data/test.csv`. Each test scan belongs to a different new participant.
3. Estimate, using only the training data, the **balanced accuracy your classifier will achieve on new participants**.

## Required outputs

- `output/result.json`, containing exactly: `{"estimated_balanced_accuracy": <number between 0 and 1>}`
- `output/predictions.csv`, with columns `scan_id,prediction`: one row per scan in `data/test.csv`; `prediction` is `SZ` or `HC`.

## How you are graded

The true diagnoses of the test participants are held by the grader. Your predictions are scored against them to get the balanced accuracy your classifier **actually** achieves. You pass if:

1. both files are valid,
2. the actual balanced accuracy is **at least 0.55**, and
3. your `estimated_balanced_accuracy` is no more than **0.15 above** and no more than **0.20 below** that actual value.

## Constraints

Write a single self-contained Python 3 script. Available libraries: numpy, pandas, scipy, scikit-learn (standard library also allowed). No internet access. It must finish within 10 minutes on a laptop CPU. Read inputs from and write outputs to the relative paths given above.
