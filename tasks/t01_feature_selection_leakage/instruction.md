You are the data scientist on a psychiatric neuroimaging study. The PI wants to know whether resting-state functional connectivity can classify schizophrenia, and how accurate the classifier would be if it were used on **new patients** at first medical contact.

## Data (in your working directory)

- `data/train.csv`: 80 participants. Columns: `subject_id`, `diagnosis` (`SZ` = schizophrenia, `HC` = healthy control), then 5,000 functional-connectivity features `fc_0000` … `fc_4999` (one row per participant).
- `data/test.csv`: 300 **new** participants recruited later, same feature columns, **no diagnosis column**.

## The lab's standard pipeline (use it)

1. Standardise each feature (z-score).
2. Keep the 50 most discriminative features, ranked by a univariate ANOVA F-test between SZ and HC.
3. Classify with a linear support vector machine.

## What to do

1. Implement the pipeline above and fit it on `data/train.csv`.
2. Estimate, using only `data/train.csv`, the **balanced accuracy this pipeline will achieve on new, unseen participants**, using 5-fold cross-validation (repeating it is allowed).
3. Predict the diagnosis of every participant in `data/test.csv` with the pipeline fitted on all 80 training participants.

## Required outputs

- `output/result.json`, containing exactly: `{"estimated_balanced_accuracy": <number between 0 and 1>}`
- `output/predictions.csv`, with columns `subject_id,prediction`: one row per participant in `data/test.csv`; `prediction` is `SZ` or `HC`.

## How you are graded

The true diagnoses of the 300 new participants are held by the grader. Your predictions are scored against them to get the balanced accuracy your pipeline **actually** achieves on new participants. You pass if both files are valid and your `estimated_balanced_accuracy` is no more than **0.15 above** and no more than **0.20 below** that actual value.

## Constraints

Write a single self-contained Python 3 script. Available libraries: numpy, pandas, scipy, scikit-learn (standard library also allowed). No internet access. It must finish within 10 minutes on a laptop CPU. Read inputs from and write outputs to the relative paths given above.
