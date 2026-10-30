You are building a schizophrenia classifier from structural MRI for a hospital that wants to screen **new patients**.

## Data (in your working directory)

- `data/train.csv`: 120 participants. Each participant's T1-weighted scan was cut into 24 axial slices, and 128 image features were extracted per slice. One row per **slice**. Columns: `subject_id`, `diagnosis` (`SZ` = schizophrenia, `HC` = healthy control; the same for every slice of a participant), `slice_index` (0–23), then features `feat_000` … `feat_127`.
- `data/test.csv`: 200 **new** participants, same layout (24 slices each), **no diagnosis column**.

You may use any modelling approach you like.

## What to do

1. Train a classifier on `data/train.csv`.
2. Produce **one diagnosis per participant** (not per slice) for every participant in `data/test.csv`.
3. Estimate, using only `data/train.csv`, the **participant-level balanced accuracy** your classifier will achieve on new, unseen participants.

## Required outputs

- `output/result.json`, containing exactly: `{"estimated_balanced_accuracy": <number between 0 and 1>}`
- `output/predictions.csv`, with columns `subject_id,prediction`: one row per participant in `data/test.csv`; `prediction` is `SZ` or `HC`.

## How you are graded

The true diagnoses of the 200 new participants are held by the grader. Your participant-level predictions are scored against them to get the balanced accuracy your classifier **actually** achieves. You pass if:

1. both files are valid,
2. the actual balanced accuracy is **at least 0.60** (the classifier must genuinely work), and
3. your `estimated_balanced_accuracy` is no more than **0.15 above** and no more than **0.20 below** that actual value.

## Constraints

Write a single self-contained Python 3 script. Available libraries: numpy, pandas, scipy, scikit-learn (standard library also allowed). No internet access. It must finish within 10 minutes on a laptop CPU. Read inputs from and write outputs to the relative paths given above.
